import {initializeApp} from "https://www.gstatic.com/firebasejs/9.9.3/firebase-app.js";
import {
    getFirestore,
} from "https://www.gstatic.com/firebasejs/9.9.3/firebase-firestore.js";
// Import Firebase Config from init.js
import { FIREBASE_CONFIG } from "./init.js";

// Initialize Firebase
const app = initializeApp(FIREBASE_CONFIG);
const db = getFirestore(app);

export default db;