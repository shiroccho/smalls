<?php
// データベース接続を取得
function getDB() {
    return new SQLite3('kanban.db');
}

// タスクを取得
function getTasks() {
    $db = getDB();
    $result = $db->query('SELECT * FROM tasks ORDER BY id ASC');
    
    $tasks = [
        '予定' => [],
        '進行中' => [],
        '完了' => [],
        '保留' => []
    ];
    
    while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
        $tasks[$row['status']][] = $row;
    }
    
    return $tasks;
}

// タスクを追加
function addTask($title, $description, $status) {
    $db = getDB();
    $stmt = $db->prepare('INSERT INTO tasks (title, description, status) VALUES (:title, :description, :status)');
    $stmt->bindValue(':title', $title, SQLITE3_TEXT);
    $stmt->bindValue(':description', $description, SQLITE3_TEXT);
    $stmt->bindValue(':status', $status, SQLITE3_TEXT);
    return $stmt->execute();
}

// タスクを更新
function updateTask($id, $title, $description, $status) {
    $db = getDB();
    $stmt = $db->prepare('UPDATE tasks SET title = :title, description = :description, status = :status, updated_at = CURRENT_TIMESTAMP WHERE id = :id');
    $stmt->bindValue(':id', $id, SQLITE3_INTEGER);
    $stmt->bindValue(':title', $title, SQLITE3_TEXT);
    $stmt->bindValue(':description', $description, SQLITE3_TEXT);
    $stmt->bindValue(':status', $status, SQLITE3_TEXT);
    return $stmt->execute();
}

// タスクを移動
function moveTask($id, $newStatus) {
    $db = getDB();
    $stmt = $db->prepare('UPDATE tasks SET status = :status, updated_at = CURRENT_TIMESTAMP WHERE id = :id');
    $stmt->bindValue(':id', $id, SQLITE3_INTEGER);
    $stmt->bindValue(':status', $newStatus, SQLITE3_TEXT);
    return $stmt->execute();
}

// タスクを削除
function deleteTask($id) {
    $db = getDB();
    $stmt = $db->prepare('DELETE FROM tasks WHERE id = :id');
    $stmt->bindValue(':id', $id, SQLITE3_INTEGER);
    return $stmt->execute();
}

// タスクを取得（単一）
function getTaskById($id) {
    $db = getDB();
    $stmt = $db->prepare('SELECT * FROM tasks WHERE id = :id');
    $stmt->bindValue(':id', $id, SQLITE3_INTEGER);
    $result = $stmt->execute();
    return $result->fetchArray(SQLITE3_ASSOC);
}
?>
