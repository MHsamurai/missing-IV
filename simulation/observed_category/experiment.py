"""Candidate observed-category model; no old block bridge is used.

DAG: (W,Z) -> F -> (Y1,Y2,Y3), (Y1,Yj) -> Dj.
Estimation maximizes the constrained observed-data mixture likelihood.
The saturated logistic and unrestricted binary selection-cell models coincide.
"""
from pathlib import Path
from itertools import product
import argparse
import json
import hashlib
import platform
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import pandas as pd
import scipy
from scipy.special import expit, logit
from scipy.optimize import minimize, brentq

ROOT = Path(__file__).resolve().parent
OBS = np.array(list(product(range(4), range(2), range(3), range(3))))
HIDDEN = np.array(list(product(range(2), range(2), range(2))))
V = OBS[:, 0]
F = np.broadcast_to(HIDDEN[None, :, 0], (72, 8))
Y = np.stack([np.broadcast_to(OBS[:, None, 1], (72, 8)),
              np.broadcast_to(HIDDEN[None, :, 1], (72, 8)),
              np.broadcast_to(HIDDEN[None, :, 2], (72, 8))], axis=2)
D = (OBS[:, 2:] != 2).astype(int)
MATCH = np.all((OBS[:, None, 2:] == 2) | (OBS[:, None, 2:] == Y[:, :, 1:]), axis=2)
METHODS = ['oracle', 'MAR_ignorability', 'selection_misspecified', 'candidate_saturated']


def config():
    return json.loads((ROOT / 'config.yml').read_text())


def truth(c, mechanism):
    m = np.array(c['measurement'])
    lam = np.array(c['class2_given_v'])
    pv = np.array(c['v_probability'])
    pf = np.array([1 - pv @ lam, pv @ lam])
    pi = np.empty((2, 2, 2))
    beta = np.array(c['selection_coefficients'])
    for j in range(2):
        weights = np.array([[np.sum(pf * (m[0] if a else 1-m[0]) *
                               (m[j+1] if y else 1-m[j+1])) for y in range(2)] for a in range(2)])
        eta = np.array([[0 if mechanism == 'MCAR' else beta[0]*a +
                        (beta[1]*y+beta[2]*a*y if mechanism == 'MNAR' else 0)
                        for y in range(2)] for a in range(2)])
        alpha = brentq(lambda b: np.sum(weights * expit(b+eta)) - c['nonanchor_response_rate'], -15, 15)
        pi[j] = expit(alpha+eta)
    return m, lam, pi


def unpack(theta, method):
    m, lam = expit(theta[:6]).reshape(3, 2), expit(theta[6:10])
    if method == 'candidate_saturated':
        pi = expit(theta[10:]).reshape(2, 2, 2)
    elif method == 'selection_misspecified':
        # A free intercept and Yj slope, but no Y1 terms.
        pi = np.repeat(expit(theta[10:]).reshape(2, 1, 2), 2, axis=1)
    else:
        pi = np.ones((2, 2, 2))
    return m, lam, pi


def probability_score(theta, method):
    m, lam, pi = unpack(theta, method)
    p = np.where(F == 1, lam[V, None], 1-lam[V, None]) * MATCH
    score = np.zeros((72, 8, len(theta)))
    for j in range(3):
        mj = m[j, F]
        p = p * np.where(Y[:, :, j] == 1, mj, 1-mj)
        for f in range(2):
            score[:, :, 2*j+f] = (F == f) * (Y[:, :, j]-mj)
    for v in range(4):
        score[:, :, 6+v] = (V[:, None] == v) * (F-lam[v])
    if method in ('candidate_saturated', 'selection_misspecified'):
        for j in range(2):
            pij = pi[j, Y[:, :, 0], Y[:, :, j+1]]
            p = p * np.where(D[:, None, j] == 1, pij, 1-pij)
            for a in range(2 if method == 'candidate_saturated' else 1):
                for y in range(2):
                    index = 10 + (4*j+2*a+y if method == 'candidate_saturated' else 2*j+y)
                    mask = (Y[:, :, j+1] == y)
                    if method == 'candidate_saturated':
                        mask = mask & (Y[:, :, 0] == a)
                    score[:, :, index] = mask * (D[:, None, j]-pij)
    prob = np.maximum(p.sum(axis=1), 1e-300)
    obs_score = np.einsum('oh,ohp->op', p, score) / prob[:, None]
    return prob, obs_score


def objective(theta, counts, method):
    p, s = probability_score(theta, method)
    return -counts @ np.log(p) / counts.sum(), -counts @ s / counts.sum()


def fit(counts, method, rng, starts=6, maxiter=1500):
    candidates = []
    for _ in range(starts):
        m = np.column_stack([rng.uniform(.1, .45, 3), rng.uniform(.55, .9, 3)])
        lam = rng.uniform(.15, .85, 4)
        t = np.r_[logit(m.ravel()), logit(lam)]
        if method in ('candidate_saturated', 'selection_misspecified'):
            t = np.r_[t, logit(rng.uniform(.55, .85, 8 if method == 'candidate_saturated' else 4))]
        res = minimize(objective, t, args=(counts, method), jac=True, method='L-BFGS-B',
                       bounds=[(-10, 10)]*len(t),
                       options={'maxiter': maxiter, 'ftol': 1e-12, 'gtol': 1e-7})
        candidates.append(res)
    best = min(candidates, key=lambda r: r.fun)
    return best, candidates


def targets(theta, method, pv):
    m, lam, _ = unpack(theta, method)
    if m[1, 0] > m[1, 1]:
        m, lam = m[:, ::-1], 1-lam
    pf = pv @ lam
    mean = m @ np.array([1-pf, pf])
    cells = np.array([np.sum(np.array([1-pf, pf]) * np.prod(np.where(np.array(y)[:, None], m, 1-m), axis=0))
                      for y in product(range(2), repeat=3)])
    return np.r_[m.ravel(), pf, mean, cells]


NAMES = [f'M{j+1}_class{f+1}' for j in range(3) for f in range(2)] + ['p_class2'] + \
        [f'mean_Y{j+1}' for j in range(3)] + ['P'+''.join(map(str, y)) for y in product(range(2), repeat=3)]


def inference(theta, counts, method, pv):
    # Joint sandwich includes the empirical distribution of always-observed V.
    h = 1e-4
    eye = np.eye(len(theta))*h
    H = np.column_stack([(objective(theta+e, counts, method)[1]-objective(theta-e, counts, method)[1])/(2*h) for e in eye])
    H = (H+H.T)/2
    mineig = np.linalg.eigvalsh(H)[0]
    if mineig <= 1e-9 or np.max(np.abs(theta)) >= 9.9:
        return np.full(len(NAMES), np.nan), mineig
    _, scores = probability_score(theta, method)
    influence_theta = scores @ np.linalg.inv(H).T
    jac = np.column_stack([(targets(theta+e, method, pv)-targets(theta-e, method, pv))/(2*h) for e in eye])
    influence = influence_theta @ jac.T
    for v in range(4):
        ep = np.eye(4)[v]*h
        derivative = (targets(theta, method, pv+ep)-targets(theta, method, pv-ep))/(2*h)
        influence += ((V == v)-pv[v])[:, None]*derivative
    influence -= counts @ influence / counts.sum()
    variance = np.sum(counts[:, None]*influence**2, axis=0)/counts.sum()**2
    return np.sqrt(variance), mineig


def sample(c, mechanism, rng):
    m, lam, pi = truth(c, mechanism)
    n = c['sample_size']
    v = rng.choice(4, n, p=c['v_probability'])
    f = (rng.random(n) < lam[v]).astype(int)
    y = (rng.random((n, 3)) < m[:, f].T).astype(int)
    d = rng.random((n, 2)) < np.column_stack([pi[j, y[:, 0], y[:, j+1]] for j in range(2)])
    t = np.where(d, y[:, 1:], 2)
    obs_index = ((v*2+y[:, 0])*3+t[:, 0])*3+t[:, 1]
    oracle_index = ((v*2+y[:, 0])*3+y[:, 1])*3+y[:, 2]
    return (np.bincount(obs_index, minlength=72), np.bincount(oracle_index, minlength=72),
            np.bincount(v, minlength=4)/n, (1+d.sum(axis=1)).mean()/3,
            np.all(d, axis=1).mean())


def population_checks(c, mechanism):
    m, lam, pi = truth(c, mechanism)
    pv = np.array(c['v_probability'])
    theta = np.r_[logit(m.ravel()), logit(lam), logit(pi.ravel())]
    prob, _ = probability_score(theta, 'candidate_saturated')
    joint = (prob*pv[V]).reshape(4, 2, 3, 3)
    assert np.isclose(joint.sum(), 1)
    pf = np.array([1-pv @ lam, pv @ lam])
    g = np.column_stack([pv*(1-lam)/pf[0], pv*lam/pf[1]])
    rows, recovered = [], []
    for a in range(2):
        tensor = joint[:, a].transpose(1, 2, 0)
        pa = tensor.sum()
        tensor /= pa
        # Independent matrix-pencil CP recovery from observable tensor only.
        s = tensor.sum(axis=2)
        u, _, vt = np.linalg.svd(s)
        u, v = u[:, :2], vt.T[:, :2]
        weighted = np.einsum('ijv,v->ij', tensor, np.arange(4))
        pencil = (u.T @ weighted @ v) @ np.linalg.inv(u.T @ s @ v)
        _, eigenvectors = np.linalg.eig(pencil)
        k2 = np.real(u @ eigenvectors)
        k2 /= k2.sum(axis=0)
        weighted_k3 = np.linalg.pinv(k2) @ s
        omega = weighted_k3.sum(axis=1)
        k3 = (weighted_k3 / omega[:, None]).T
        ghat = np.stack([(np.linalg.pinv(k2) @ tensor[:, :, v]).sum(axis=1)/omega for v in range(4)])
        kernels, pis = [], []
        for j, k in enumerate([k2, k3]):
            inverse_pi = np.linalg.solve(k[:2].T, np.ones(2))
            kernels.append(k[:2]*inverse_pi[:, None])
            pis.append(1/inverse_pi)
            truek = np.vstack([(1-m[j+1])*pi[j, a, 0], m[j+1]*pi[j, a, 1],
                               1-(1-m[j+1])*pi[j, a, 0]-m[j+1]*pi[j, a, 1]])
            rows.append({'mechanism': mechanism, 'stratum': a, 'matrix': f'K{j+2}',
                         'rank': int(np.linalg.matrix_rank(truek)), 'sigma_min': np.linalg.svd(truek, compute_uv=False)[-1],
                         'inverse_determinant': np.linalg.det(truek[:2].T)})
        order = np.argsort(kernels[0][1])
        for j in range(2):
            assert np.max(np.abs(kernels[j][1, order]-m[j+1])) < 1e-9
            assert np.max(np.abs(pis[j]-pi[j, a])) < 1e-9
        assert np.max(np.abs(ghat[:, order]-g)) < 1e-9
        recovered.append((pa, omega[order]))
    recovered_pf = sum(pa*omega for pa, omega in recovered)
    assert np.max(np.abs(recovered_pf-pf)) < 1e-9
    recovered_m1 = recovered[1][0]*recovered[1][1]/recovered_pf
    assert np.max(np.abs(recovered_m1-m[0])) < 1e-9
    rows.append({'mechanism': mechanism, 'stratum': 'both', 'matrix': 'G',
                 'rank': int(np.linalg.matrix_rank(g)), 'sigma_min': np.linalg.svd(g, compute_uv=False)[-1]})
    # The old arbitrary four-cell block completeness still fails.
    for j in [1, 2]:
        b = np.array([[(1-lam[v])*np.prod([(m[k, 0] if y else 1-m[k, 0]) for k, y in zip([0, j], cell)])+
                      lam[v]*np.prod([(m[k, 1] if y else 1-m[k, 1]) for k, y in zip([0, j], cell)])
                      for cell in product(range(2), repeat=2)] for v in range(4)])
        rows.append({'mechanism': mechanism, 'stratum': 'fixed X', 'matrix': f'old_pair_1{j+1}',
                     'rank': int(np.linalg.matrix_rank(b)), 'sigma_min': np.linalg.svd(b, compute_uv=False)[-1]})
    return rows


def run_one(job):
    c, mechanism, rep = job
    # Common complete data and response uniforms across the three mechanisms.
    rng = np.random.default_rng(np.random.SeedSequence([c['seed'], rep]))
    counts, oracle, pv, rate, complete_rate = sample(c, mechanism, rng)
    m, lam, pi = truth(c, mechanism)
    true_theta = np.r_[logit(m.ravel()), logit(lam), logit(pi.ravel())]
    actual = targets(true_theta, 'candidate_saturated', np.array(c['v_probability']))
    rows, diagnostics = [], []
    for method in METHODS:
        used = oracle if method == 'oracle' else counts
        best, candidates = fit(used, method, rng, c['starts'], c['maxiter'])
        estimate = targets(best.x, method, pv)
        se, eigenvalue = inference(best.x, used, method, pv)
        stationary = bool(best.success and np.max(np.abs(best.jac)) < 1e-5)
        if not stationary:
            se[:] = np.nan
        diagnostics.append({'mechanism': mechanism, 'rep': rep, 'method': method, 'success': bool(best.success),
                            'gradient_max': np.max(np.abs(best.jac)), 'boundary': np.max(np.abs(best.x)) >= 9.9,
                            'hessian_min': eigenvalue, 'valid_se': bool(np.all(np.isfinite(se))),
                            'nll': best.fun, 'start_nll_range': max(r.fun for r in candidates)-best.fun,
                            'item_rate': rate, 'complete_rate': complete_rate,
                            'stationary': stationary,
                            'boundary_parameters': ','.join(map(str, np.flatnonzero(np.abs(best.x) >= 9.9)))})
        for name, target, value, error in zip(NAMES, actual, estimate, se):
            rows.append({'mechanism': mechanism, 'rep': rep, 'method': method, 'parameter': name,
                         'truth': target, 'estimate': value, 'se': error,
                         'covered': float(abs(value-target) <= 1.96*error) if np.isfinite(error) else np.nan})
    return rows, diagnostics


def run(c, directory='results'):
    out = ROOT / directory
    out.mkdir(exist_ok=True)
    pd.DataFrame([r for mechanism in c['mechanisms'] for r in population_checks(c, mechanism)]).to_csv(out/'rank_checks.csv', index=False)
    rows, diagnostics = [], []
    jobs = [(c, mechanism, rep) for mechanism in c['mechanisms'] for rep in range(c['replications'])]
    with ProcessPoolExecutor(max_workers=c['workers']) as pool:
        for i, (r, d) in enumerate(pool.map(run_one, jobs), 1):
            rows.extend(r)
            diagnostics.extend(d)
            if i % 10 == 0:
                print(f'{i}/{len(jobs)} datasets', flush=True)
                pd.DataFrame(rows).to_csv(out/'estimates.csv', index=False)
                pd.DataFrame(diagnostics).to_csv(out/'diagnostics.csv', index=False)
    data = pd.DataFrame(rows)
    data.to_csv(out/'estimates.csv', index=False)
    pd.DataFrame(diagnostics).to_csv(out/'diagnostics.csv', index=False)
    result = []
    for (mechanism, method, parameter), g in data.groupby(['mechanism', 'method', 'parameter']):
        error = g.estimate-g.truth
        result.append(dict(mechanism=mechanism, method=method, parameter=parameter, bias=error.mean(),
                           RMSE=np.sqrt(np.mean(error**2)), SD=g.estimate.std(), estimated_SE=g.se.mean(),
                           coverage_valid=g.covered.mean(), valid_CI=g.covered.notna().sum(),
                           SD_valid=g.loc[g.covered.notna(), 'estimate'].std(),
                           CI_failure_rate=g.covered.isna().mean(),
                           covered_and_available=g.covered.fillna(0).mean(),
                           bias_MCSE=g.estimate.std()/np.sqrt(len(g)), replications=len(g)))
    pd.DataFrame(result).to_csv(out/'summary.csv', index=False)
    (out/'run_config.json').write_text(json.dumps(c, indent=2))
    metadata = {'python': platform.python_version(), 'numpy': np.__version__,
                'scipy': scipy.__version__, 'pandas': pd.__version__,
                'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (out/'provenance.json').write_text(json.dumps(metadata, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--replications', type=int)
    parser.add_argument('--sample-size', type=int)
    parser.add_argument('--output', default='results')
    args = parser.parse_args()
    c = config()
    if args.replications:
        c['replications'] = args.replications
    if args.sample_size:
        c['sample_size'] = args.sample_size
    run(c, args.output)
