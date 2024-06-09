-- Создание FTS таблицы
CREATE VIRTUAL TABLE Films_fts USING fts3(id, name, description);

INSERT INTO Films_fts (rowid, id, name, description)
SELECT id, id, name, description FROM Films;


-- Триггеры для вставки, обновления и удаления данных в FTS таблице
CREATE TRIGGER films_ai AFTER INSERT ON Films BEGIN
  INSERT INTO Films_fts (rowid, id, name, description) VALUES (new.id, new.id, new.name, new.description);
END;

CREATE TRIGGER films_ad AFTER DELETE ON Films BEGIN
  DELETE FROM Films_fts WHERE rowid = old.id;
END;

CREATE TRIGGER films_au AFTER UPDATE ON Films BEGIN
  UPDATE Films_fts SET id = new.id, name = new.name, description = new.description WHERE rowid = old.id;
END;