import { type NextRequest, NextResponse } from "next/server";

export async function middleware(req: NextRequest) {
  const destination = req.nextUrl.pathname;
  const referer = req.headers.get("referer");

  if (referer === "/dashboard") {
    if (!referer || !referer.includes("/auth/login")) {
      const token = req.cookies.get("TOKEN")?.value || "";
      const username = req.cookies.get("Username")?.value || "";

      if (!token || !username) {
        console.log("Missing credentials");
        return NextResponse.redirect(new URL("/auth/login", req.url));
      }

      const response = await fetch(
        "http://127.0.0.1:9090/api/user/authenticate",
        {
          method: "POST",
          credentials: "include",
          headers: {
            Username: username,
            TOKEN: token,
          },
        },
      );

      if (response.status === 202) {
        console.log("Authenticated");
        return NextResponse.next();
      } else {
        console.log("Invalid credentials");
        return NextResponse.redirect(new URL("/auth/login", req.url));
      }
    }
  } else if (destination.startsWith("/auth/register/")) {
    const path_components = destination.split("/");
    const invite_id = path_components[path_components.length - 1];

    const response = await fetch(
      "http://127.0.0.1:9090/api/user/check_invite",
      {
        method: "GET",
        credentials: "include",
        headers: {
          url: invite_id,
        },
      },
    );

    if (response.status === 202) {
      return NextResponse.next();
    } else {
      return NextResponse.redirect(new URL("/auth/login", req.url));
    }
  }
}

export const config = {
  matcher: ["/dashboard", "/auth/register/:path*"],
};
