import {
    collection, onSnapshot, query, where, updateDoc, doc,
} from "https://www.gstatic.com/firebasejs/9.9.3/firebase-firestore.js";
import db from './fire-base-config.js'

// global variable
let totalNotification = 0;

const notificationsRef = collection(db, "users", `${currentSuperuserId}`, "notifications")
const allQuery = query(notificationsRef, where("is_deleted", "==", false), where("is_read", "==", false));
onSnapshot(allQuery, (querySnapshot) => {
    let count = 0;
    querySnapshot.forEach((doc) => {
        count = count + 1
    });
    totalNotification = count;

    if (totalNotification > 0) {
        document.getElementById("total-notifications").innerHTML = `<span class="badge rounded-pill text-bg-danger">${totalNotification}</span>`;
    }
});

const updateStatusNotification = async (key) => {
    await updateDoc(doc(db, "users", `${currentSuperuserId}`, "notifications", key), {
        is_read: true
    });
}


const showDetail = (item) => {
    const showPopup = (title, content, image, key, callBackFunc, bntTitle = "Ok", showCancelButton = false) => {

        Swal.fire({
            title: title,
            text: content,
            imageUrl: image,
            imageWidth: '120px',
            confirmButtonColor: "#417690",
            showCancelButton: showCancelButton,
            confirmButtonText: bntTitle,
            allowOutsideClick: false
        }).then((result) => {
            if (result.isConfirmed) {
                callBackFunc();
            }
        })

    }

    const type = item.type;
    switch (type) {
        case 'SYSTEM':
            showPopup(item?.title, item?.content, item?.image, item?.key, () => {
                const jobPostId = item[type].job_post_id
                updateStatusNotification(item.key)
            });
            break;
        case 'POST_VERIFY_REQUIRED':
            showPopup(item?.title, item?.content, item?.image, item?.key, () => {
                const jobPostId = item[type].job_post_id
                updateStatusNotification(item.key)
                window.location.href = `/admin/job/jobpost/${jobPostId}/change/`;
            }, "Go to censorship", true);
            break;
        default:
            break;
    }
}

export {showDetail};
