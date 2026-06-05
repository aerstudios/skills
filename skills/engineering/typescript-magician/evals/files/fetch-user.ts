type User = {
    id: number;
    name: string;
    email: string;
};

async function fetchUser(userId: string): Promise<any> {
    const response = await fetch(`/api/users/${userId}`);
    return response.json();
}

export async function loadUserName(userId: string) {
    const user = await fetchUser(userId);
    return user.name.toUpperCase();
}