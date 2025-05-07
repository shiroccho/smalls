<?php
// データベース接続
$db_file = 'kakeibo.db';
$pdo = new PDO('sqlite:' . $db_file);
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

// 削除処理
if (isset($_GET['delete']) && is_numeric($_GET['delete'])) {
    $stmt = $pdo->prepare('DELETE FROM transactions WHERE id = ?');
    $stmt->execute([$_GET['delete']]);
    header('Location: index.php');
    exit;
}

// 総収支を計算
$stmt = $pdo->query('SELECT SUM(amount) as total FROM transactions');
$totalBalance = $stmt->fetch(PDO::FETCH_ASSOC)['total'] ?? 0;

// トランザクション一覧取得
$stmt = $pdo->query('SELECT * FROM transactions ORDER BY created_at DESC');
$transactions = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>

<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>お小遣い帳</title>
    <style>
        body {
            font-family: 'Helvetica Neue', Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .balance {
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            margin: 20px 0;
            padding: 10px;
            background-color: #fff;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .balance-positive {
            color: #28a745;
        }
        .balance-negative {
            color: #dc3545;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background-color: white;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            border-radius: 5px;
        }
        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f8f9fa;
        }
        tr:hover {
            background-color: #f1f1f1;
        }
        .type-income {
            background-color: #d4edda;
            color: #155724;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 0.8em;
        }
        .type-expense {
            background-color: #f8d7da;
            color: #721c24;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 0.8em;
        }
        .amount {
            font-weight: bold;
        }
        .amount-income {
            color: #28a745;
        }
        .amount-expense {
            color: #dc3545;
        }
        .btn {
            display: inline-block;
            padding: 8px 12px;
            background-color: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            font-size: 14px;
            border: none;
            cursor: pointer;
        }
        .btn-danger {
            background-color: #dc3545;
        }
        .btn-success {
            background-color: #28a745;
        }
        .actions {
            display: flex;
            gap: 5px;
        }
        .footer {
            margin-top: 20px;
            text-align: center;
        }
    </style>
</head>
<body>
    <h1>お小遣い帳</h1>

    <div class="header">
        <a href="add.php" class="btn btn-success">新規登録</a>
    </div>

    <div class="balance <?= $totalBalance >= 0 ? 'balance-positive' : 'balance-negative' ?>">
        現在の総収支: <?= number_format($totalBalance) ?> 円
    </div>

    <table>
        <thead>
            <tr>
                <th>日付</th>
                <th>区分</th>
                <th>金額</th>
                <th>メモ</th>
                <th>操作</th>
            </tr>
        </thead>
        <tbody>
            <?php if (empty($transactions)): ?>
                <tr>
                    <td colspan="5" style="text-align: center;">データがありません</td>
                </tr>
            <?php else: ?>
                <?php foreach ($transactions as $transaction): ?>
                    <tr>
                        <td><?= date('Y/m/d', strtotime($transaction['created_at'])) ?></td>
                        <td>
                            <?php if ($transaction['type'] === 'income'): ?>
                                <span class="type-income">入金</span>
                            <?php else: ?>
                                <span class="type-expense">出金</span>
                            <?php endif; ?>
                        </td>
                        <td class="amount <?= $transaction['type'] === 'income' ? 'amount-income' : 'amount-expense' ?>">
                            <?= $transaction['type'] === 'income' ? '+' : '-' ?><?= number_format(abs($transaction['amount'])) ?> 円
                        </td>
                        <td><?= htmlspecialchars($transaction['memo']) ?></td>
                        <td class="actions">
                            <a href="edit.php?id=<?= $transaction['id'] ?>" class="btn">編集</a>
                            <a href="index.php?delete=<?= $transaction['id'] ?>" class="btn btn-danger" onclick="return confirm('本当に削除しますか？')">削除</a>
                        </td>
                    </tr>
                <?php endforeach; ?>
            <?php endif; ?>
        </tbody>
    </table>

    <div class="footer">
        <a href="export.php" class="btn">CSV出力</a>
    </div>
</body>
</html>
