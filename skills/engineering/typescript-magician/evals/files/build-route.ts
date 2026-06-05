const routes = {
    user: "/users/:id",
    postComment: "/posts/:postId/comments/:commentId",
} as const;

export function buildRoute(routeName: string, params: Record<string, string>) {
    let route = routes[routeName];

    for (const [paramName, paramValue] of Object.entries(params)) {
        route = route.replace(`:${paramName}`, paramValue);
    }

    return route;
}

buildRoute("user", { id: "123" });
buildRoute("postComment", { postId: "10" });