CREATE TABLE similar_creatures (
    base_id INTEGER NOT NULL,
    similar_id INTEGER NOT NULL,
    similarity REAL NOT NULL CHECK(similarity >= 0 AND similarity <= 1),
    PRIMARY KEY (base_id, similar_id),
    FOREIGN KEY (base_id) REFERENCES creatures(id),
    FOREIGN KEY (similar_id) REFERENCES creatures(id),
    CHECK(base_id != similar_id)
);