import axios from "axios";
import { baseURL } from "../constants/urls";

export const apiService = axios.create({ baseURL });
