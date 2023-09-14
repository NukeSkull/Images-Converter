import {toast} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export const notifyError = (startMessage, error) => {
    toast.error(startMessage + error);
};

export const notifySuccess = (message) => {
    toast.success(message);
};