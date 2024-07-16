import React, { useState } from 'react';
import "./Collapsible.css"

const CollapsibleMenu = ({ title, children }) => {
    const [isOpen, setIsOpen] = useState(false);

    const toggleMenu = () => {
        setIsOpen(!isOpen)
    };

    return (
        <div className='collapsible-menu'>
            <button onClick={toggleMenu} className='menu-title'>
                {title}
            </button>
            {isOpen && <div className='menu-content'>{children}</div>}
        </div>
    );
};

export default CollapsibleMenu