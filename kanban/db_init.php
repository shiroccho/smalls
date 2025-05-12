// db_init.php - データベースの初期化
<?php
// データベースファイル
$db_file = 'kanban.db';

// データベース接続
$db = new SQLite3($db_file);

// タスクテーブルの作成
$db->exec('
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT "予定",
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)');

// 初期データの挿入（テスト用）
$db->exec('
INSERT OR IGNORE INTO tasks (id, title, description, status) VALUES 
(1, "プロジェクト計画", "新しいプロジェクトの計画書を作成する", "予定"),
(2, "デザイン作成", "ウェブサイトのデザインを作成", "進行中"),
(3, "コーディング", "フロントエンドのコーディング", "進行中"),
(4, "テスト", "機能テストを実施", "保留"),
(5, "ドキュメント作成", "ユーザーマニュアルの作成", "完了")
');

echo "データベースが初期化されました。";
?>
