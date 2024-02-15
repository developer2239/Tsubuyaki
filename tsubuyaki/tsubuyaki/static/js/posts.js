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