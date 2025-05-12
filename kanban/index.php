<?php
require_once 'functions.php';

// POSTリクエストの処理
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // タスクの追加
    if (isset($_POST['action']) && $_POST['action'] === 'add') {
        $title = $_POST['title'];
        $description = $_POST['description'];
        $status = $_POST['status'];
        addTask($title, $description, $status);
    }
    // タスクの更新
    elseif (isset($_POST['action']) && $_POST['action'] === 'update') {
        $id = $_POST['id'];
        $title = $_POST['title'];
        $description = $_POST['description'];
        $status = $_POST['status'];
        updateTask($id, $title, $description, $status);
    }
    // タスクの削除
    elseif (isset($_POST['action']) && $_POST['action'] === 'delete') {
        $id = $_POST['id'];
        deleteTask($id);
    }
    // タスクの移動（ステータス変更）
    elseif (isset($_POST['action']) && $_POST['action'] === 'move') {
        $id = $_POST['id'];
        $newStatus = $_POST['new_status'];
        moveTask($id, $newStatus);
    }
    
    // リダイレクトしてPOSTの再送信を防止
    header('Location: index.php');
    exit;
}

// タスクの編集モードか確認
$editMode = false;
$editTask = null;
if (isset($_GET['edit']) && !empty($_GET['edit'])) {
    $editMode = true;
    $editTask = getTaskById($_GET['edit']);
}

// すべてのタスクを取得
$tasks = getTasks();
?>

<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>シンプルカンバンアプリ</title>
    <link rel="stylesheet" href="style.css">
    <script>
        // タスクのドラッグ&ドロップ用のJavaScript
        function allowDrop(ev) {
            ev.preventDefault();
        }
        
        function drag(ev) {
            ev.dataTransfer.setData("taskId", ev.target.getAttribute("data-id"));
            // ドラッグ中のアイテムに効果を追加
            ev.target.classList.add("dragging");
        }
        
        function dragEnd(ev) {
            // ドラッグ終了時にクラスを削除
            ev.target.classList.remove("dragging");
        }
        
        function drop(ev) {
            ev.preventDefault();
            
            // ドロップターゲットを見つける
            let dropTarget = ev.target;
            let newStatus = "";
            
            // ドロップ先がタスクカードの場合は親要素（column-content）を取得
            if (dropTarget.classList.contains("task-card") || 
                dropTarget.classList.contains("task-title") || 
                dropTarget.classList.contains("task-description") ||
                dropTarget.classList.contains("task-actions")) {
                
                while (dropTarget && !dropTarget.classList.contains("column-content")) {
                    dropTarget = dropTarget.parentElement;
                }
            }
            
            // カラムのdata-status属性を取得
            if (dropTarget && dropTarget.hasAttribute("data-status")) {
                newStatus = dropTarget.getAttribute("data-status");
            } else {
                // 適切なドロップ対象でなければ終了
                return;
            }
            
            const taskId = ev.dataTransfer.getData("taskId");
            if (!taskId || !newStatus) return;
            
            // フォームを作成して送信
            const form = document.createElement('form');
            form.method = 'post';
            form.action = 'index.php';
            
            const actionInput = document.createElement('input');
            actionInput.type = 'hidden';
            actionInput.name = 'action';
            actionInput.value = 'move';
            form.appendChild(actionInput);
            
            const idInput = document.createElement('input');
            idInput.type = 'hidden';
            idInput.name = 'id';
            idInput.value = taskId;
            form.appendChild(idInput);
            
            const statusInput = document.createElement('input');
            statusInput.type = 'hidden';
            statusInput.name = 'new_status';
            statusInput.value = newStatus;
            form.appendChild(statusInput);
            
            document.body.appendChild(form);
            form.submit();
        }
        
        // 画面ロード時にイベントリスナーを追加
        document.addEventListener('DOMContentLoaded', function() {
            // すべてのドラッグ可能なタスクにdragendイベントを追加
            const draggableItems = document.querySelectorAll('.task-card[draggable="true"]');
            for (let item of draggableItems) {
                item.addEventListener('dragend', dragEnd);
            }
            
            // すべてのカラムにドロップイベントを追加
            const columns = document.querySelectorAll('.column-content');
            for (let column of columns) {
                column.addEventListener('drop', drop);
                column.addEventListener('dragover', allowDrop);
            }
        });
        
        // タスク編集用モーダル
        function openEditModal(id) {
            document.getElementById("editModal").style.display = "block";
            // タスク情報を取得してモーダルに表示する処理を追加
        }
        
        function closeEditModal() {
            document.getElementById("editModal").style.display = "none";
        }
    </script>
</head>
<body>
    <h1>シンプルカンバンアプリ</h1>
    
    <!-- タスク追加フォーム -->
    <div class="form-container">
        <h2><?php echo $editMode ? 'タスクを編集' : '新しいタスクを追加'; ?></h2>
        <form method="post">
            <input type="hidden" name="action" value="<?php echo $editMode ? 'update' : 'add'; ?>">
            <?php if ($editMode): ?>
                <input type="hidden" name="id" value="<?php echo $editTask['id']; ?>">
            <?php endif; ?>
            
            <div class="form-group">
                <label for="title">タイトル</label>
                <input type="text" id="title" name="title" required value="<?php echo $editMode ? htmlspecialchars($editTask['title']) : ''; ?>">
            </div>
            
            <div class="form-group">
                <label for="description">説明</label>
                <textarea id="description" name="description" rows="3"><?php echo $editMode ? htmlspecialchars($editTask['description']) : ''; ?></textarea>
            </div>
            
            <div class="form-group">
                <label for="status">ステータス</label>
                <select id="status" name="status">
                    <option value="予定" <?php echo ($editMode && $editTask['status'] === '予定') ? 'selected' : ''; ?>>予定</option>
                    <option value="進行中" <?php echo ($editMode && $editTask['status'] === '進行中') ? 'selected' : ''; ?>>進行中</option>
                    <option value="完了" <?php echo ($editMode && $editTask['status'] === '完了') ? 'selected' : ''; ?>>完了</option>
                    <option value="保留" <?php echo ($editMode && $editTask['status'] === '保留') ? 'selected' : ''; ?>>保留</option>
                </select>
            </div>
            
            <button type="submit" class="btn"><?php echo $editMode ? '更新' : '追加'; ?></button>
            <?php if ($editMode): ?>
                <a href="index.php" class="btn" style="background-color: #6c757d; margin-left: 10px;">キャンセル</a>
            <?php endif; ?>
        </form>
    </div>
    
    <!-- カンバンボード -->
    <div class="kanban-container">
        <?php
        $statuses = ['予定', '進行中', '完了', '保留'];
        foreach ($statuses as $status):
        ?>
        <div class="kanban-column">
            <div class="column-header"><?php echo $status; ?></div>
            <div class="column-content" data-status="<?php echo $status; ?>">
                <?php if (empty($tasks[$status])): ?>
                <div class="empty-column-message" style="padding: 20px; text-align: center; color: #999;">
                    タスクをここにドラッグ
                </div>
                <?php else: ?>
                <?php foreach ($tasks[$status] as $task): ?>
                <div class="task-card" draggable="true" ondragstart="drag(event)" data-id="<?php echo $task['id']; ?>">
                    <div class="task-title"><?php echo htmlspecialchars($task['title']); ?></div>
                    <div class="task-description"><?php echo htmlspecialchars($task['description']); ?></div>
                    <div class="task-actions">
                        <a href="index.php?edit=<?php echo $task['id']; ?>">編集</a>
                        <form method="post" style="display: inline;" onsubmit="return confirm('このタスクを削除してもよろしいですか？');">
                            <input type="hidden" name="action" value="delete">
                            <input type="hidden" name="id" value="<?php echo $task['id']; ?>">
                            <button type="submit" style="background: none; border: none; color: #dc3545; text-decoration: none; font-size: 0.8em; cursor: pointer;">削除</button>
                        </form>
                    </div>
                </div>
                <?php endforeach; ?>
                <?php endif; ?>
            </div>
        </div>
        <?php endforeach; ?>
    </div>
</body>
</html>
