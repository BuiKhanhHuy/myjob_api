import {initializeApp} from "https://www.gstatic.com/firebasejs/9.9.3/firebase-app.js";
import {
    getDatabase, ref, query, orderByChild, limitToFirst, startAt, get, onValue, remove,
} from "https://www.gstatic.com/firebasejs/9.9.3/firebase-database.js";

const firebaseConfig = {
    apiKey: 'AIzaSyCKr_uSX5ObUgxEEfLIOYhze750NPlTjgM',
    authDomain: 'myjobpro-6283b.firebaseapp.com',
    projectId: 'myjobpro-6283b',
    storageBucket: 'myjobpro-6283b.appspot.com',
    messagingSenderId: '734184453591',
    appId: '1:734184453591:web:226041c4414b54c9b8c792',
    databaseURL: 'https://myjobpro-6283b-default-rtdb.asia-southeast1.firebasedatabase.app/',
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const database = getDatabase(app);


const PAGE_SIZE = 5;
let lastKey = null;
let notifications = []

window.onload = () => {
    const notificationsRef = ref(database, `notifications/${1}`);

    // Lắng nghe thay đổi danh sách thông báo
    let notificationsQuery = query(notificationsRef, orderByChild('time'), limitToFirst(PAGE_SIZE));
    onValue(notificationsQuery, (snapshot) => {
        const data = snapshot.val();

        if (data) {
            const newNotifications = Object.values(data).map((notification) => ({
                ...notification, key: Object.keys(data).find((key) => data[key] === notification),
            }));

            toastr.info('There is a new notification.')
            console.log(newNotifications)
            renderItems(newNotifications || [])
        } else {
            renderItems(notifications)
        }
    });

    // Lắng nghe sự thay đổi số lượng thông báo
    let countNotificationsQuery = query(notificationsRef, orderByChild('time'));
    onValue(countNotificationsQuery, (snapshot) => {
        const data = snapshot.val();
        const countNoti = data ? Object.keys(data).length : 0;

    });
}

const handleLoadMore = () => {
    const lastKeyInList = notifications[notifications.length - 1].time;
    if (lastKeyInList !== lastKey) {
        lastKey = lastKeyInList + 1;
    }

    const notificationsRef = ref(database, `notifications/${1}`);
    let notificationsQuery = query(notificationsRef, orderByChild('time'), limitToFirst(PAGE_SIZE));

    if (lastKey) {
        notificationsQuery = query(notificationsRef, orderByChild('time'), startAt(lastKey), limitToFirst(PAGE_SIZE));
    }

    const getNotifications = async () => {
        const snapshot = await get(notificationsQuery);
        const data = snapshot.val();
        if (data) {
            const newNotifications = Object.values(data).map((notification) => ({
                ...notification, key: Object.keys(data).find((key) => data[key] === notification),
            }));
            notifications = [...notifications, ...newNotifications];
            renderItems(notifications)
        }
    };

    getNotifications().then(r => console.log(r));
}

const renderItems = (data) => {
    let strItem = (item) => {
        // let createdAt = moment(`${item.time}`).fromNow()
        let createdAt = item.time;


        return ` <li class="mb-2" onclick="">
                    <a class="dropdown-item border-radius-md" href="javascript:;">
                        <div class="d-flex py-1">
                            <div class="my-auto">
                                <img alt="img" src=" ${item?.image}"
                                     class="avatar avatar-lg  me-3 "/>
                            </div>
                            <div class="d-flex flex-column justify-content-center">
                                <h6 class="text-sm font-weight-normal mb-1">
                                    <span class="font-weight-bold">${item?.title || '---'}</span>
                                </h6>
                                <p class="text-sm font-weight-normal mb-1">
                                    ${item?.content || '---'}
                                </p>
                                <p class="text-xs text-secondary mb-0">
                                    <i class="fa fa-clock me-1"></i>
                                    ${createdAt}
                                </p>
                            </div>
                        </div>
                    </a>
                </li>`


    }
    let strContent = ''
    let notificationContent = document.getElementById('notification-content')

    for (let i = 0; i < data.length; i++) {
        strContent += strItem(data[i])
    }
    notificationContent.innerHTML = strContent;
}
