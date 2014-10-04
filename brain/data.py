def simple_lr(samples):
    """
    Returns linear regression coefficients (b, a) where f = bx + a

    samples :: [(Float, Float)]
    """
    xs, ys = list(map(lambda a: a[0], samples)), list(map(lambda a: a[1], samples))
    avgx = sum(xs) / len(xs)
    avgy = sum(ys) / len(ys)
    bnum = sum([(xs[i] - avgx) * (ys[i] - avgy) for i in range(len(samples))])
    bdenom = sum([(xs[i] - avgx) ** 2 for i in range(len(samples))])
    b = bnum / bdenom
    a = avgy - b * avgx
    return (b, a)
