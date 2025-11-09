def choose_one_hash(hashes: dict[str, str]) -> dict[str, str] | None:
    if "MD5" in hashes:
        return {"MD5": hashes["MD5"]}
    if "SHA-1" in hashes:
        return {"SHA-1": hashes["SHA-1"]}
    if "SHA-256" in hashes:
        return {"SHA-256": hashes["SHA-256"]}
    if "SHA-512" in hashes:
        return {"SHA-512": hashes["SHA-512"]}

    k = next(iter(hashes), None)
    if k is not None:
        return {k: hashes[k]}

    return None
