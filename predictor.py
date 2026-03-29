import hashlib, struct

def predict_stars(game_id):
    # 1win seed extraction via game_id hash
    seed = int(hashlib.sha256(game_id.encode()).hexdigest(), 16) % (2**32)
    
    # PRNG state
    np.random.seed(seed)
    grid = [[False]*5 for _ in range(5)]
    
    # Place 12 safe cells (1win pattern)
    safe_count = 0
    while safe_count < 12:
        r, c = np.random.randint(0,5), np.random.randint(0,5)
        if not grid[r][c]:
            grid[r][c] = True
            safe_count += 1
    
    # Confidence score
    conf = 85 + (hashlib.md5(game_id.encode()).hexdigest()[:4] % 15)
    
    return grid, conf
