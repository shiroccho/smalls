<?php
// データベース接続
$db_file = 'kakeibo.db';
$pdo = new PDO('sqlite:' . $db_file);
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

// トランザクション一覧取得
$stmt = $pdo->query('SELECT * FROM transactions ORDER BY created_at DESC');
$transactions = $stmt->fetchAll(PDO::FETCH_ASSOC);

// CSVファイル名設定
$filename = 'kakeibo_export_' . date('Ymd_His') . '.csv';

// ヘッダー設定
header('Content-Type: text/csv; charset=UTF-8');
header('Content-Disposition: attachment; filename="' . $filename . '"');

// 出力バッファを開始
ob_start();

// UTF-8 BOMを出力 (Excel対応)
echo "\xEF\xBB\xBF";

// CSVヘッダー行
$headers = ['ID', '日付', '区分', '金額(円)', 'メモ'];
echo implode(',', $headers) . "\n";

// データ行
foreach ($transactions as $transaction) {
    $type = $transaction['amount'] >= 0 ? '入金' : '出金';
    $amount = abs($transaction['amount']);
    $date = date('Y/m/d', strtotime($transaction['created_at']));
    
    // CSVエスケープ処理
    $memo = str_replace('"', '""', $transaction['memo']);
    if (strpos($memo, ',') !== false || strpos($memo, '"') !== false || strpos($memo, "\n") !== false) {
        $memo = '"' . $memo . '"';
    }
    
    $line = [
        $transaction['id'],
        $date,
        $type,
        $amount,
        $memo
    ];
    
    echo implode(',', $line) . "\n";
}

// ファイルに出力して終了
$csv = ob_get_clean();
echo $csv;
exit();
