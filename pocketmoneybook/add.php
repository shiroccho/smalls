<?php
// データベース接続
$db_file = 'kakeibo.db';
$pdo = new PDO('sqlite:' . $db_file);
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$error = '';
$success = false;

// フォーム送信時の処理
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $type = $_POST['type'] ?? 'expense';
    $amount = isset($_POST['amount']) ? filter_var($_POST['amount'], FILTER_VALIDATE_INT) : null;
    $memo = $_POST['memo'] ?? '';

    if ($amount === false || $amount === null || $amount <= 0) {
        $error = '金額は正の整数で入力してください。';
    } else {
        try {
            $realAmount = ($type === 'income') ? $amount : -$amount;
            
            $stmt = $pdo->prepare('INSERT INTO transactions (amount, type, memo) VALUES (?, ?, ?)');
            $stmt->execute([$realAmount, $type, $memo]);
            
            $success = true;
            
            // 登録成功したら一覧ページにリダイレクト
            header('Location: index.php');
            exit;
        } catch (PDOException $e) {
            $error = 'データベースエラー: ' . $e->getMessage();
        }
    }
}
?>

<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>新規登録 - お小遣い帳</title>
    <style>
        body {
            font-family: 'Helvetica Neue', Arial, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .form-container {
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="text"],
        input[type="number"],
        textarea {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        .radio-group {
            display: flex;
            gap: 15px;
        }
        .radio-label {
            display: flex;
            align-items: center;
            cursor: pointer;
        }
        .radio-label input {
            margin-right: 5px;
        }
        .btn {
            display: inline-block;
            padding: 10px 15px;
            background-color: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            font-size: 16px;
            border: none;
            cursor: pointer;
        }
        .btn-success {
            background-color: #28a745;
        }
        .btn-secondary {
            background-color: #6c757d;
        }
        .footer {
            margin-top: 20px;
            display: flex;
            justify-content: space-between;
        }
        .error {
            color: #dc3545;
            margin-bottom: 15px;
        }
        .success {
            color: #28a745;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <h1>新規登録</h1>

    <div class="form-container">
        <?php if ($error): ?>
            <div class="error"><?= $error ?></div>
        <?php endif; ?>
        
        <?php if ($success): ?>
            <div class="success">登録が完了しました</div>
        <?php endif; ?>

        <form method="post">
            <div class="form-group">
                <label>区分</label>
                <div class="radio-group">
                    <label class="radio-label">
                        <input type="radio" name="type" value="income"> 入金
                    </label>
                    <label class="radio-label">
                        <input type="radio" name="type" value="expense" checked> 出金
                    </label>
                </div>
            </div>
            
            <div class="form-group">
                <label for="amount">金額 (円)</label>
                <input type="number" id="amount" name="amount" min="1" required>
            </div>
            
            <div class="form-group">
                <label for="memo">メモ</label>
                <textarea id="memo" name="memo" rows="3"></textarea>
            </div>
            
            <div class="footer">
                <a href="index.php" class="btn btn-secondary">キャンセル</a>
                <button type="submit" class="btn btn-success">登録</button>
            </div>
        </form>
    </div>
</body>
</html>
