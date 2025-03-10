"use client";

import React, { useCallback } from "react";
import Image from "next/image";
import { MdSpaceDashboard } from "react-icons/md";
import { IoLogOut } from "react-icons/io5";
import { useRouter } from "next/navigation";
import cookieManager from "../cookie_manager";

type TabParams = {
  icon: React.ReactElement;
  path: string;
};

/**
 * This file contains the components for the sidebar navigation.
 * Components included:
 * - Logo: Displays a logo image.
 * - Seperator: Displays a separator.
 * - Tab: Displays a tab with an icon and a link.
 * - Navbar: Displays the navigation bar.
 */

/**
 * Logo component that displays a logo image.
 * @param icon - The path to the logo image.
 * @returns A React element containing the logo image.
 */
function Logo({ icon }: { icon: string }) {
  return (
    <div className="items-center bg-opacity-0 p-3 order-first m-1">
      <Image
        src={icon}
        alt="icon"
        height={48}
        width={48}
        unoptimized
        priority
      />
    </div>
  );
}

/**
 * Seperator component that displays a separator.
 * @returns A React element containing the separator.
 */
function Seperator() {
  return <div className="w-20 h-6 bg-opacity-0" />;
}

/**
 * Tab component that displays a tab with an icon and a link.
 * @param icon - The icon to display inside the tab.
 * @param path - The path to navigate to when the tab is clicked.
 * @returns A React element containing the tab.
 */
function Tab({ icon, path }: TabParams) {
  return (
    <div className="flex items-center justify-center relative size-12 hover:size-14 ease-out transition-all duration-150 group">
      <div className="absolute size-9 blur-none rounded-full group-hover:blur-md group-hover:bg-schemes-dark-on-surface-variant ease-out transition-all duration-150" />
      <a
        href={path}
        className="relative bg-schemes-dark-surface-container-lowest rounded-full size-12 flex items-center justify-center ease-out group-hover:size-14 group-hover:bg-schemes-dark-surface-variant transition-all duration-150"
      >
        {icon}
      </a>
    </div>
  );
}

/**
 * Navbar component that displays the navigation bar.
 * @returns A React element containing the navigation bar.
 */
export default function Navbar() {
  const router = useRouter();

  /**
   * Handles the click event for the logout button.
   * Clears the authentication cookies and redirects to the login page.
   * Memoized to prevent unnecessary re-renders.
   *
   * @param event - The mouse event triggered by clicking the button.
   */
  const handleClick = useCallback(
    async (event: React.MouseEvent<HTMLAnchorElement>) => {
      event.preventDefault();

      const user = (await cookieManager.getCookie("Username"))?.toString();
      const token = (await cookieManager.getCookie("TOKEN"))?.toString();

      if (!user || !token) {
        router.push("/auth/login");
        return;
      }

      await fetch("http://127.0.0.1:5090/api/user/login", {
        method: "GET",
        credentials: "include",
        headers: {
          Username: user || "",
          TOKEN: token || "",
        },
      });

      router.push("/auth/login");
    },
    [router],
  );

  return (
    <div className="fixed flex flex-col bg-schemes-dark-background h-full w-20 items-center justify-start border-r-[1px] border-schemes-dark-surface-container-low">
      <div className="flex flex-col bg-schemes-dark-background h-full w-20 items-center justify-start border-r-[1px] border-schemes-dark-surface-container-low">
        <Logo icon="/icons/icon.png" />
        <Seperator />
        <div className="flex flex-col items-center justify-center gap-3">
          <Tab
            icon={
              <MdSpaceDashboard className="size-8 text-schemes-dark-on-background" />
            }
            path="/dashboard"
          />
        </div>
      </div>
      <div className="flex items-center justify-center size-12 hover:size-14 ease-out transition-all duration-150 group rotate-180 pt-6 cursor-context-pointer">
        <div className="absolute size-9 blur-none rounded-full group-hover:blur-md group-hover:bg-schemes-dark-on-surface-variant ease-out transition-all duration-150" />
        <a
          onClick={handleClick}
          className="relative bg-schemes-dark-surface-container-lowest rounded-full size-12 flex items-center justify-center ease-out group-hover:size-14 group-hover:bg-schemes-dark-surface-variant transition-all duration-150"
        >
          <IoLogOut className="size-8 text-schemes-dark-on-background" />
        </a>
      </div>
    </div>
  );
}
