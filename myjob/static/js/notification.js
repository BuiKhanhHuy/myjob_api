import {
    collection, getDocs, limit, onSnapshot, query, where, startAfter, orderBy, updateDoc, doc,
} from "https://www.gstatic.com/firebasejs/9.9.3/firebase-firestore.js";
import db from './fire-base-config.js'

// Popup
// global variable
const PAGE_SIZE = 5;
let totalNotification = 0;
let lastVisible = null;
let notifications = [];

const notificationsRef = collection(db, "users", `${currentSuperuserId}`, "notifications")
const first = query(notificationsRef, where("is_deleted", "==", false), where("is_read", "==", false), orderBy('time', 'desc'), limit(PAGE_SIZE));

const allQuery = query(notificationsRef, where("is_deleted", "==", false), where("is_read", "==", false));
onSnapshot(allQuery, (querySnapshot) => {
    let count = 0;
    querySnapshot.forEach((doc) => {
        count = count + 1
    });
    totalNotification = count;

    document.getElementById("total-notification").innerHTML = totalNotification;
});

console.log("LOAD NOTIFICATIONS OF POPUP")
const unsubscribe = onSnapshot(first, (querySnapshot) => {
    const notificationList = [];
    querySnapshot.forEach((doc) => {
        notificationList.push({
            ...doc.data(), key: doc.id
        });
    });
    notifications = notificationList;

    // hiển thị thông báo
    renderItems(notifications)

    // Get the last visible document
    lastVisible = querySnapshot.docs[querySnapshot.docs.length - 1];
});


// Load more button click event
document.getElementById("load-more").addEventListener("click", async () => {
    if (lastVisible) {
        const nextQuery = query(collection(db, "users", `${currentSuperuserId}`, "notifications"),
            where("is_deleted", "==", false),
            where("is_read", "==", false),
            orderBy('time', 'desc'),
            startAfter(lastVisible),
            limit(PAGE_SIZE));
        const nextQuerySnapshot = await getDocs(nextQuery);

        const nextNotificationList = [];
        nextQuerySnapshot.forEach((doc) => {
            nextNotificationList.push({
                ...doc.data(), key: doc.id
            });
        });

        notifications = notifications.concat(nextNotificationList);
        // hiển thị thông báo
        renderItems(notifications)

        lastVisible = nextQuerySnapshot.docs[nextQuerySnapshot.docs.length - 1];
    }
});

const renderItems = (data) => {
    let strItem = (item) => {

        return `<li class="mb-2" id="${'notification-detail-' + item?.key}">
                    <a class="dropdown-item border-radius-md" href="javascript:;" >
                        <div class="d-flex py-1">
                            <div class="my-auto me-1" style="width: 100px;">
                                <img alt="img" src="${item?.image}"  
                                     class="avatar avatar-lg img-fluid"/>
                            </div>
                            <div class="d-flex flex-column justify-content-center" >
                                <h6 class="text-sm font-weight-normal mb-1" >
                                    <span class="font-weight-bold">${item?.title || '---'}</span>
                                </h6>
                                <p class="text-sm font-weight-normal mb-1 " style="white-space: normal;" >
                                    ${item?.content || '---'}
                                </p>
                                <p class="text-xs text-secondary mb-0">
                                    <i class="fa fa-clock me-1"></i>
                                    ${moment(new Date(item?.time?.seconds * 1000)).fromNow()}
                                </p>
                               
                            </div>
                        </div>  
                    </a>
                </li>`


    }
    let strContent = ''
    if (data.length <= 0) {
        strContent = '<li><a class="dropdown-item border-radius-md" href="javascript:;" ><div class="text-center my-2">No notifications.</div></a></li>'
    }
    let notificationContent = document.getElementById('notification-content')

    for (let i = 0; i < data.length; i++) {
        strContent += strItem(data[i])
    }
    notificationContent.innerHTML = strContent;

    // them xu kien cho action la xem chi tiet
    for (let i = 0; i < data.length; i++) {
        document.getElementById(`notification-detail-${data[i].key}`).addEventListener("click", () => showDetail(data[i]));
    }

    // an hoac hien button xem them
    let btnLoadMore = document.getElementById('load-more')
    if (Math.ceil(totalNotification / PAGE_SIZE) > 1) {
        btnLoadMore.style.display = 'block'
    } else {
        btnLoadMore.style.display = 'none'
    }
}

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
            imageWidth: 85,
            imageHeight: 85,
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
