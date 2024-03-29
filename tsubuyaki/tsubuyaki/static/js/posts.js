/**
 * お気に入りの追加・解除
 * @param {*} postId 
 */
async function favorite(postId){
    isDeleted = false;
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
    const res = await fetch("/favorite/", postData)
        .then(function (data){
            return data.json();
        })
        .then(function (json){
            if(json["is_error_happened"]){
                alert("エラーが発生しました。再度お試しください。")
            } else { 
                let countTextNode = document.getElementById(postId);
                let textSpan = document.createElement("span");
                textSpan.setAttribute("id",postId);
                textSpan.appendChild(document.createTextNode(json["favorite_count"]));
                countTextNode.replaceWith(textSpan);
            }
        });
}

/**
 * 引数で指定されたpostIdをオフセットとして、そこから古い順に20件取得する
 * @param {*} postId 呟き情報ID
 * @returns 読み込んだ最後のpostId
 */
async function fetchPosts(postId){
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
    return await fetch("/fetch_posts/", postData)
        .then(function (data) {
            return data.json(); // 読み込むデータをJSONに設定
        })
        .then(function (json) {
            let last_postId = postId;
            const posts = JSON.parse(json["posts"]);
            for(const post of posts){
                createPostPanel(post);
                last_postId = post["post_id"];
            }
            if(postId != null){
                const oldleadMoreButton = document.getElementById("lead_more_button");
                oldleadMoreButton.remove();
            }
            if (!json["is_last"]) {
                let newLeadMoreButton = document.createElement("button");
                newLeadMoreButton.setAttribute("id","lead_more_button");
                newLeadMoreButton.className = "lead_more_button";
                newLeadMoreButton.addEventListener("click",function(){
                    fetchPosts(last_postId);
                });
                newLeadMoreButton.appendChild(document.createTextNode("さらに読み込む"))
                let leadMore = document.getElementById("lead_more");
                leadMore.appendChild(newLeadMoreButton);
            }
        });
}

/**
 * 呟きのエレメントを作成し、コンテントに追加
 * @param {*} post
 */
function createPostPanel(post){

    // ユーザ情報
    let userInfo = document.createElement("div");
    userInfo.className = "user_info";
    userInfo.addEventListener('click', function() {
        location.href = '/profile/?account_id=' + post["account_id"];
    });
    userInfo.textContent =  post["name"] + "@" + post["id"];
    // 本文
    let postText = document.createElement("div");
    postText.className = "post_text";
    postText.textContent = post["post_content"];
    // 日時
    let postDate = document.createElement("div");
    postDate.className = "post_date";
    postDate.textContent = post["created_at"];
    // いいねボタン
    let favoriteButton = document.createElement("div");
    favoriteButton.className = "favorite_button";
    let favoriteButtonIcon = document.createElementNS("http://www.w3.org/2000/svg","svg");
    favoriteButtonIcon.setAttribute("width","12");
    favoriteButtonIcon.setAttribute("height","12");
    favoriteButtonIcon.setAttribute("fill","currentColor");
    favoriteButtonIcon.setAttribute("viewBox","0 0 16 16");
    favoriteButtonIcon.addEventListener("click",
    function(){
        favorite(post["post_id"]);
    });
    elmPath = document.createElementNS("http://www.w3.org/2000/svg", 'path');
    elmPath.setAttribute('d', 'M8.864.046C7.908-.193 7.02.53 6.956 1.466c-.072 1.051-.23 2.016-.428 2.59-.125.36-.479 1.013-1.04 1.639-.557.623-1.282 1.178-2.131 1.41C2.685 7.288 2 7.87 2 8.72v4.001c0 .845.682 1.464 1.448 1.545 1.07.114 1.564.415 2.068.723l.048.03c.272.165.578.348.97.484.397.136.861.217 1.466.217h3.5c.937 0 1.599-.477 1.934-1.064a1.86 1.86 0 0 0 .254-.912c0-.152-.023-.312-.077-.464.201-.263.38-.578.488-.901.11-.33.172-.762.004-1.149.069-.13.12-.269.159-.403.077-.27.113-.568.113-.857 0-.288-.036-.585-.113-.856a2.144 2.144 0 0 0-.138-.362 1.9 1.9 0 0 0 .234-1.734c-.206-.592-.682-1.1-1.2-1.272-.847-.282-1.803-.276-2.516-.211a9.84 9.84 0 0 0-.443.05 9.365 9.365 0 0 0-.062-4.509A1.38 1.38 0 0 0 9.125.111L8.864.046zM11.5 14.721H8c-.51 0-.863-.069-1.14-.164-.281-.097-.506-.228-.776-.393l-.04-.024c-.555-.339-1.198-.731-2.49-.868-.333-.036-.554-.29-.554-.55V8.72c0-.254.226-.543.62-.65 1.095-.3 1.977-.996 2.614-1.708.635-.71 1.064-1.475 1.238-1.978.243-.7.407-1.768.482-2.85.025-.362.36-.594.667-.518l.262.066c.16.04.258.143.288.255a8.34 8.34 0 0 1-.145 4.725.5.5 0 0 0 .595.644l.003-.001.014-.003.058-.014a8.908 8.908 0 0 1 1.036-.157c.663-.06 1.457-.054 2.11.164.175.058.45.3.57.65.107.308.087.67-.266 1.022l-.353.353.353.354c.043.043.105.141.154.315.048.167.075.37.075.581 0 .212-.027.414-.075.582-.05.174-.111.272-.154.315l-.353.353.353.354c.047.047.109.177.005.488a2.224 2.224 0 0 1-.505.805l-.353.353.353.354c.006.005.041.05.041.17a.866.866 0 0 1-.121.416c-.165.288-.503.56-1.066.56z');
    favoriteButtonIcon.appendChild(elmPath);
    favoriteButton.appendChild(favoriteButtonIcon);
    const conutTextNode = document.createElement("span");
    conutTextNode.setAttribute("id",post["post_id"])
    conutTextNode.appendChild(document.createTextNode(post["favorite_count"]));
    favoriteButton.appendChild(conutTextNode);

    // ラッパー
    let wrapper = document.createElement("div");
    wrapper.className = "post";
    wrapper.appendChild(userInfo);
    wrapper.appendChild(postText);
    wrapper.appendChild(postDate);
    wrapper.appendChild(favoriteButton);

    // コンテントに追加
    let contents = document.getElementById("contents");
    contents.appendChild(wrapper);
}



// 初期ロード20件
fetchPosts();