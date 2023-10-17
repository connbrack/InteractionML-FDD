// from: https://svelte.dev/tutorial/writable-stores
import { writable } from 'svelte/store';

// Global
export const serverIP = 'http://127.0.0.1:5000';

//View Data
export const persistentDataSensor = writable('SA_TEMP');
export const viewDataSensorData = writable([]);