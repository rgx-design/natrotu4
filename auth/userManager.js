const API_BASE_URL = 'http://localhost:5000/api';
const TOKEN_KEY = 'naruto3_token';
const CURRENT_USER_KEY = 'naruto3_current_user';

class UserManager {
    constructor() {
        this.token = this.loadToken();
        this.currentUser = this.loadCurrentUser();
    }

    loadToken() {
        return localStorage.getItem(TOKEN_KEY);
    }

    saveToken(token) {
        localStorage.setItem(TOKEN_KEY, token);
        this.token = token;
    }

    removeToken() {
        localStorage.removeItem(TOKEN_KEY);
        this.token = null;
    }

    loadCurrentUser() {
        const data = localStorage.getItem(CURRENT_USER_KEY);
        return data ? JSON.parse(data) : null;
    }

    saveCurrentUser(user) {
        localStorage.setItem(CURRENT_USER_KEY, JSON.stringify(user));
        this.currentUser = user;
    }

    removeCurrentUser() {
        localStorage.removeItem(CURRENT_USER_KEY);
        this.currentUser = null;
    }

    async register(username, email, password) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, email, password })
            });

            const data = await response.json();

            if (data.success) {
                this.saveToken(data.token);
                this.saveCurrentUser(data.user);
            }

            return data;
        } catch (error) {
            return { success: false, message: '网络错误，请稍后重试' };
        }
    }

    async login(usernameOrEmail, password) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ usernameOrEmail, password })
            });

            const data = await response.json();

            if (data.success) {
                this.saveToken(data.token);
                this.saveCurrentUser(data.user);
            }

            return data;
        } catch (error) {
            return { success: false, message: '网络错误，请稍后重试' };
        }
    }

    logout() {
        this.removeToken();
        this.removeCurrentUser();
    }

    async getUserProgress(userId) {
        try {
            const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            const data = await response.json();

            if (data.success) {
                return data.user;
            }

            return null;
        } catch (error) {
            return null;
        }
    }

    async getAllUsers() {
        try {
            const response = await fetch(`${API_BASE_URL}/users/`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            const data = await response.json();

            if (data.success) {
                return data.users;
            }

            return [];
        } catch (error) {
            return [];
        }
    }

    async getMe() {
        try {
            const response = await fetch(`${API_BASE_URL}/users/me`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            const data = await response.json();

            if (data.success) {
                this.saveCurrentUser(data.user);
                return data.user;
            }

            return null;
        } catch (error) {
            return null;
        }
    }

    async updatePoints(data) {
        try {
            const response = await fetch(`${API_BASE_URL}/users/me/points`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                this.saveCurrentUser(result.user);
            }

            return result;
        } catch (error) {
            return { success: false, message: '网络错误' };
        }
    }

    async updateUser(data) {
        try {
            const response = await fetch(`${API_BASE_URL}/users/me`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                this.saveCurrentUser(result.user);
            }

            return result;
        } catch (error) {
            return { success: false, message: '网络错误' };
        }
    }

    async updateProgress(data) {
        if (this.currentUser) {
            const updatedUser = { ...this.currentUser, ...data };
            this.saveCurrentUser(updatedUser);
            await this.updateUser(data);
        }
    }

    getCustomWordbooks() {
        return [];
    }

    async forgotPassword(email) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/forgotpassword`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email })
            });

            return await response.json();
        } catch (error) {
            return { success: false, message: '网络错误' };
        }
    }

    async resetPassword(token, password) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/resetpassword/${token}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ password })
            });

            return await response.json();
        } catch (error) {
            return { success: false, message: '网络错误' };
        }
    }

    getUser(username) {
        return this.currentUser && this.currentUser.username === username ? this.currentUser : null;
    }

    getUserProgress(user) {
        return this.currentUser;
    }
}

const userManager = new UserManager();