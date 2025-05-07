<?php
header('Content-Type: text/html; charset=UTF-8');

echo '<html>';
echo '<head>';
echo '<title>SQLite3動作確認</title>';
echo '<style>
body {
    font-family: sans-serif;
    margin: 20px;
    line-height: 1.6;
}
h1 {
    color: #333;
    border-bottom: 1px solid #ddd;
    padding-bottom: 10px;
}
.section {
    margin-bottom: 20px;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 5px;
}
.success {
    background-color: #dff0d8;
    border-color: #d6e9c6;
    color: #3c763d;
}
.error {
    background-color: #f2dede;
    border-color: #ebccd1;
    color: #a94442;
}
.info {
    background-color: #d9edf7;
    border-color: #bce8f1;
    color: #31708f;
}
.details {
    margin-top: 10px;
    font-family: monospace;
    white-space: pre-wrap;
    background-color: #f5f5f5;
    padding: 10px;
    border-radius: 3px;
}
table {
    border-collapse: collapse;
    width: 100%;
}
table, th, td {
    border: 1px solid #ddd;
}
th, td {
    padding: 8px;
    text-align: left;
}
th {
    background-color: #f2f2f2;
}
</style>';
echo '</head>';
echo '<body>';
echo '<h1>SQLite3動作確認</h1>';

// PHP バージョン表示
echo '<div class="section info">';
echo '<h2>PHP環境情報</h2>';
echo 'PHP バージョン: ' . phpversion();
echo '<div class="details">';
echo 'サーバーソフトウェア: ' . $_SERVER['SERVER_SOFTWARE'] . '<br>';
echo 'OS: ' . PHP_OS . '<br>';
echo '</div>';
echo '</div>';

// SQLite3 拡張モジュールのチェック
echo '<div class="section ' . (extension_loaded('sqlite3') ? 'success' : 'error') . '">';
echo '<h2>SQLite3拡張モジュール</h2>';
if (extension_loaded('sqlite3')) {
    echo 'SQLite3 拡張モジュールは<strong>有効</strong>です。';
    echo '<div class="details">';
    echo 'SQLite バージョン: ' . SQLite3::version()['versionString'] . '<br>';
    echo '</div>';
} else {
    echo 'SQLite3 拡張モジュールは<strong>無効</strong>です。';
}
echo '</div>';

// PDO SQLite ドライバのチェック
echo '<div class="section ' . (in_array('sqlite', PDO::getAvailableDrivers()) ? 'success' : 'error') . '">';
echo '<h2>PDO SQLiteドライバ</h2>';
if (in_array('sqlite', PDO::getAvailableDrivers())) {
    echo 'PDO SQLite ドライバは<strong>有効</strong>です。';
    echo '<div class="details">';
    echo '利用可能なPDOドライバ: ' . implode(', ', PDO::getAvailableDrivers());
    echo '</div>';
} else {
    echo 'PDO SQLite ドライバは<strong>無効</strong>です。';
}
echo '</div>';

// 実際にSQLite3データベースを作成してテストする
echo '<div class="section">';
echo '<h2>SQLite3動作テスト</h2>';

try {
    // テスト用のデータベースファイル名
    $dbFile = 'test_sqlite_' . time() . '.db';
    
    // SQLite3クラスでテスト
    echo '<h3>SQLite3クラスでのテスト:</h3>';
    if (extension_loaded('sqlite3')) {
        try {
            $db = new SQLite3($dbFile);
            $db->exec('CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)');
            $db->exec("INSERT INTO test (name) VALUES ('テストデータ')");
            $result = $db->query('SELECT * FROM test');
            $row = $result->fetchArray(SQLITE3_ASSOC);
            
            echo '<div class="success">SQLite3データベース操作に成功しました。</div>';
            echo '<div class="details">';
            echo 'テーブル作成: 成功<br>';
            echo 'データ挿入: 成功<br>';
            echo 'データ取得: ' . json_encode($row, JSON_UNESCAPED_UNICODE) . '<br>';
            echo '</div>';
            
            $db->close();
        } catch (Exception $e) {
            echo '<div class="error">SQLite3クラステスト中にエラーが発生しました: ' . $e->getMessage() . '</div>';
        }
    } else {
        echo '<div class="error">SQLite3拡張モジュールが無効なためテストできません。</div>';
    }
    
    // PDOでテスト
    echo '<h3>PDOでのテスト:</h3>';
    if (in_array('sqlite', PDO::getAvailableDrivers())) {
        try {
            $pdo = new PDO('sqlite:' . $dbFile);
            $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            
            $pdo->exec('CREATE TABLE IF NOT EXISTS test_pdo (id INTEGER PRIMARY KEY, name TEXT)');
            $pdo->exec("INSERT INTO test_pdo (name) VALUES ('PDOテストデータ')");
            
            $stmt = $pdo->query('SELECT * FROM test_pdo');
            $row = $stmt->fetch(PDO::FETCH_ASSOC);
            
            echo '<div class="success">PDO SQLiteデータベース操作に成功しました。</div>';
            echo '<div class="details">';
            echo 'テーブル作成: 成功<br>';
            echo 'データ挿入: 成功<br>';
            echo 'データ取得: ' . json_encode($row, JSON_UNESCAPED_UNICODE) . '<br>';
            echo '</div>';
            
            $pdo = null;
        } catch (PDOException $e) {
            echo '<div class="error">PDOテスト中にエラーが発生しました: ' . $e->getMessage() . '</div>';
        }
    } else {
        echo '<div class="error">PDO SQLiteドライバが無効なためテストできません。</div>';
    }
    
    // テスト後にファイルを削除
    if (file_exists($dbFile)) {
        unlink($dbFile);
        echo '<div class="info">テスト用データベースファイルを削除しました。</div>';
    }
} catch (Exception $e) {
    echo '<div class="error">テスト実行中に予期せぬエラーが発生しました: ' . $e->getMessage() . '</div>';
}
echo '</div>';

// PHPの設定情報（SQLite関連）
echo '<div class="section info">';
echo '<h2>SQLite関連PHP設定</h2>';
echo '<table>';
echo '<tr><th>設定項目</th><th>値</th></tr>';

$relevantIni = [
    'sqlite3.extension_dir',
    'pdo.dsn.*',
    'open_basedir',
    'disable_functions',
    'safe_mode'
];

foreach ($relevantIni as $ini) {
    if (strpos($ini, '*') !== false) {
        // ワイルドカードの処理
        $prefix = str_replace('*', '', $ini);
        $all = ini_get_all();
        foreach ($all as $key => $value) {
            if (strpos($key, $prefix) === 0) {
                echo '<tr><td>' . htmlspecialchars($key) . '</td><td>' . htmlspecialchars(ini_get($key)) . '</td></tr>';
            }
        }
    } else {
        echo '<tr><td>' . htmlspecialchars($ini) . '</td><td>' . htmlspecialchars(ini_get($ini)) . '</td></tr>';
    }
}

echo '</table>';
echo '</div>';

// ファイル書き込み権限テスト
echo '<div class="section">';
echo '<h2>ファイル書き込み権限テスト</h2>';

$testDir = dirname(__FILE__);
$testFile = $testDir . '/write_test_' . time() . '.tmp';

try {
    $result = @file_put_contents($testFile, 'Test');
    if ($result !== false) {
        echo '<div class="success">カレントディレクトリへの書き込みが<strong>可能</strong>です。SQLiteデータベースファイルを作成できます。</div>';
        unlink($testFile);
    } else {
        echo '<div class="error">カレントディレクトリへの書き込みが<strong>不可能</strong>です。SQLiteデータベースファイルを作成できない可能性があります。</div>';
    }
    
    echo '<div class="details">';
    echo 'テストディレクトリ: ' . htmlspecialchars($testDir) . '<br>';
    echo 'ディレクトリ権限: ' . substr(sprintf('%o', fileperms($testDir)), -4) . '<br>';
    echo '</div>';
} catch (Exception $e) {
    echo '<div class="error">書き込みテスト中にエラーが発生しました: ' . $e->getMessage() . '</div>';
}

echo '</div>';

echo '</body>';
echo '</html>';
?>
