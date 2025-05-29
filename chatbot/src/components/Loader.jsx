import React from "react";
import "./loader.css"

export default function Loader() {


    return (
        <main className="loader-main">

            <p style={{fontWeight: 'bold'}}>
                Loading...
            </p>
            <p>
                The chat api service my take some to start. Please wait or refresh the page.
            </p>
        </main>
    )
}