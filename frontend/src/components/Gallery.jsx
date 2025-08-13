import React, { useState, useEffect, useContext } from 'react';
import { LanguageContext } from '../i18n';

const Gallery = ({ items }) => {
  const [focusedIndex, setFocusedIndex] = useState(0);
  const { t } = useContext(LanguageContext);

  const handleKeyDown = (event) => {
    if (event.key === 'ArrowRight') {
      setFocusedIndex((focusedIndex + 1) % items.length);
    } else if (event.key === 'ArrowLeft') {
      setFocusedIndex((focusedIndex - 1 + items.length) % items.length);
    }
  };

  useEffect(() => {
    const current = document.getElementById(`gallery-item-${focusedIndex}`);
    if (current) {
      current.focus();
    }
  }, [focusedIndex]);

  return (
    <div role="list" aria-label={t('gallery')}>
      {items.map((item, index) => (
        <div
          key={item.id || index}
          id={`gallery-item-${index}`}
          role="listitem"
          tabIndex={index === focusedIndex ? 0 : -1}
          onKeyDown={handleKeyDown}
        >
          {item.title}
        </div>
      ))}
    </div>
  );
};

export default Gallery;

