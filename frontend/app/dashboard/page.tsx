"use client";

import React from "react";
import { FaKey } from "react-icons/fa";
import {
  Gadget,
  Greeting,
  Codeblock,
  Checkbox,
  Button,
} from "./components/page_util";

/**
 * Dashboard component that displays the main dashboard page.
 * @returns A React element containing the dashboard page.
 */
export default function Dashboard() {
  return (
    <div className="w-full h-screen bg-schemes-dark-surface-container-lowest items-start justify-start">
      <Greeting user="user" />
      <div className="grid grid-cols-1 md:grid-cols-2 items-start justify-center pt-16">
        <div className="flex flex-col items-start justify-start w-full h-full gap-9 singlecol-padding md:leftcol-padding">
          <Gadget
            title="Generate API Key"
            icon={<FaKey className="size-5 text-schemes-dark-on-background" />}
            content={
              <form
                method="POST"
                className="h-full w-full flex flex-col items-start justify-start gap-4 py-6"
              >
                <Codeblock code="https://theatre.lococto.me/ jskadfkl sdlkajl fsdlkj flsdjfklsj dlkfjskl;jf" />
                <div className="w-full h-auto flex flex-row flex-wrap items-start justify-start">
                  <Checkbox label="Permission 1" />
                  <Checkbox label="Permission 2" />
                  <Checkbox label="Permission 3" />
                  <Checkbox label="Permission 4" />
                  <Checkbox label="Permission 5" />
                </div>
                <Button label="Generate" buttontype="submit" />
              </form>
            }
          />
        </div>
        <div className="flex flex-col items-start justify-start w-full h-full gap-9 singlecol-padding md:rightcol-padding">
          <div className="gadget-desktop h-64" />
          <div className="gadget-desktop h-96" />
          <div className="gadget-desktop h-96" />
        </div>
      </div>
    </div>
  );
}
