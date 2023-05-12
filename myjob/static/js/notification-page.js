import {
    collection, getDocs, limit, onSnapshot, query, where, startAfter, orderBy, updateDoc, doc
} from "https://www.gstatic.com/firebasejs/9.9.3/firebase-firestore.js";
import db from './fire-base-config.js'
import {showDetail} from "./notification.js";

const PAGE_SIZE_PAGE = 20;
var totalNotificationPage = 0
var lastVisiblePage = null;
var notificationsPage = [];

const notificationsRef = collection(db, "users", `${currentSuperuserId}`, "notifications")
const firstPage = query(notificationsRef, where("is_deleted", "==", false), where("is_read", "in", [false, true]), orderBy('time', 'desc'), limit(PAGE_SIZE_PAGE));

const allQuery = query(notificationsRef, where("is_deleted", "==", false));
onSnapshot(allQuery, (querySnapshot) => {
    let count = 0;
    querySnapshot.forEach((doc) => {
        count = count + 1
    });
    totalNotificationPage = count;
});

onSnapshot(firstPage, (querySnapshot) => {
    const notificationList = [];
    querySnapshot.forEach((doc) => {
        notificationList.push({
            ...doc.data(), key: doc.id
        });
    });

    notificationsPage = notificationList;
    // hiển thị thông báo
    renderItemsPage(notificationsPage)

    // Get the last visible document
    lastVisiblePage = querySnapshot.docs[querySnapshot.docs.length - 1];
});


// Load more button click event
document.getElementById("load-more-page").addEventListener("click", async () => {
    if (lastVisiblePage) {
        const nextQuery = query(collection(db, "users", `${currentSuperuserId}`, "notifications"), where("is_deleted", "==", false), where("is_read", "in", [false, true]), orderBy('time', 'desc'), startAfter(lastVisiblePage), limit(PAGE_SIZE_PAGE));
        const nextQuerySnapshot = await getDocs(nextQuery);

        const nextNotificationList = [];
        nextQuerySnapshot.forEach((doc) => {
            nextNotificationList.push({
                ...doc.data(), key: doc.id
            });
        });

        notificationsPage = notificationsPage.concat(nextNotificationList);
        // hiển thị thông báo
        renderItemsPage(notificationsPage)

        lastVisiblePage = nextQuerySnapshot.docs[nextQuerySnapshot.docs.length - 1];
    }
});

const renderItemsPage = (data) => {
    let strItem = (item) => {
        // let createdAt = moment(`${item.time}`).fromNow()
        let createdAt = item.time;

        const stt = item?.is_read === true ? `<span class="badge badge-sm bg-gradient-success">Read</span>` : `<span class="badge badge-sm bg-gradient-warning">Unread</span>`

        return `<tr>
                    <td>
                      <div class="d-flex px-2 py-1">
                        <div>
                          <img src="${item?.image}" class="avatar avatar-sm me-3" alt="user1">
                        </div>
                        <div class="d-flex flex-column justify-content-center">
                          <h6 class="mb-0 text-sm">${item?.title || "---"}</h6>
                          <p class="text-xs text-secondary mb-0">${item?.content || "---"}</p>
                        </div>
                      </div>
                    </td>
                    <td class="align-middle text-center text-sm">
                     ${stt}
                    </td>
                    <td class="align-middle text-center">
                      <span class="text-secondary text-xs font-weight-bold">${moment(new Date(item?.time?.seconds * 1000)).fromNow()}</span>
                    </td>
                    <td class="align-middle text-right">
                     <a id="${'notification-delete-page-' + item?.key}" class="btn btn-link text-danger text-gradient px-3 mb-0" href="javascript:;" ><i class="far fa-trash-alt me-2"></i>Delete</a>
                      <a id="${'notification-detail-page-' + item?.key}" class="btn btn-link text-info text-gradient px-3 mb-0" href="javascript:;" "><i class="far fa-eye me-2"></i>Detail</a>
                    </td> 
                  </tr>`


    }
    let strContent = ''
    if (data.length <= 0) {
        strContent = '<tr><td colspan="4"><div class="text-center my-2">No notifications.</div></td></tr>'
    }

    let notificationContent = document.getElementById('notification-content-page')
    for (let i = 0; i < data.length; i++) {
        strContent += strItem(data[i])
    }
    notificationContent.innerHTML = strContent;

    // them xu kien cho hai action la xoa va xem chi tiet
    for (let i = 0; i < data.length; i++) {
        document.getElementById(`notification-delete-page-${data[i].key}`).addEventListener("click", () => deleteNotification(data[i].key));
        document.getElementById(`notification-detail-page-${data[i].key}`).addEventListener("click", () => showDetail(data[i]));
    }

    // an hoac hien button xem them
    let btnLoadMore = document.getElementById('load-more-page')
    if (Math.ceil(totalNotificationPage / PAGE_SIZE_PAGE) > 1) {
        btnLoadMore.style.display = 'block'
    } else {
        btnLoadMore.style.display = 'none'
    }
}

const deleteNotification = (key) => {
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
        if (result.isConfirmed) {
            updateDoc(doc(db, "users", `${currentSuperuserId}`, "notifications", key), {
                is_deleted: true
            }).then(() => {
                const index = notificationsPage.findIndex((value) => value.key === key);
                if (index > -1) {
                    let newNotifications = [...notificationsPage];
                    newNotifications.splice(index, 1);
                    notificationsPage = newNotifications;

                    renderItemsPage(notificationsPage)
                }
                Swal.fire('Deleted!', 'Your notification has been deleted.', 'success')
            })
                .catch((error) => {
                    Swal.fire({
                        icon: 'error', title: 'Oops...', text: 'Something went wrong!',
                    })
                });

        }
    })
}
