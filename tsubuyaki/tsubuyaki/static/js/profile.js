// 新しいつぶやき作成のポップアップウィンドウ
const tsubuyakiButton = document.getElementById('tsubuyaki_button');
const tsubuyakiWindow = document.getElementById('tsubuyaki_window');
const closeTsubuyakiWindowButton = document.getElementById('close_tsubuyaki_window_button')
tsubuyakiButton.addEventListener('click', function() {
    tsubuyakiWindow.style.display = 'flex';
});
closeTsubuyakiWindowButton.addEventListener('click', function() {
    tsubuyakiWindow.style.display = 'none';
});

// ポスト削除ポップアップウィンドウ
async function deletePost(postId){
    isDeleted = false
    if(confirm("このつぶやきを削除しますか？")){
        const csrftoken = Cookies.get('csrftoken');
        const postBody = {
            post_id : postId,
        };
        const postData = {
            method: "POST",
            headers : {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken,
            },
            body: JSON.stringify(postBody)
        };
        const res = await fetch("/delete/", postData)
            .then(function (data) {
                return data.json(); // 読み込むデータをJSONに設定
            })
            .then(function (json) {
                isDeleted = json["is_deleted"];
            });
        if(isDeleted){
            alert("つぶやきを削除しました");
        } else {
            alert("エラーが発生しました。既に削除されている可能性があります。")
        }
        window.location.href ='/profile/';
    }
}

// お気に入り追加・削除
async function favorite(postId){
    isDeleted = false
    const csrftoken = Cookies.get('csrftoken');
    const postBody = {
        post_id : postId,
    };
    const postData = {
        method: "POST",
        headers : {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify(postBody)
    };
    const res = await fetch("/favorite/", postData);
    window.location.reload();
}

// プロフィール変更のポップアップウィンドウ
const profileEditButton = document.getElementById('profile_edit_button');
const profileEditWindow = document.getElementById('edit_profile_window');
const closeEditProfileWindowButton = document.getElementById('close_edit_profile_window_button')
profileEditButton.addEventListener('click', function() {
    const profileText = document.getElementById('profile_profile').textContent;
    const profile = document.getElementById('profile');
    profile.textContent = profileText.trim()
    profileEditWindow.style.display = 'flex';
});
closeEditProfileWindowButton.addEventListener('click', function() {
    profileEditWindow.style.display = 'none';
});