function updateurl(user_id) {
    console.log("I am here js")
    fetch("/update_url"), {
    method: "POST",
    body: JSON.stringify({ user_id: user_id }),
    }).then ((_res) => {
    window.location.href = "/";
    })
}

