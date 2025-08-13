import { createContext, useState } from 'react';
import en from './locales/en.json';
import es from './locales/es.json';

const resources = { en, es };

export const LanguageContext = createContext({
  lang: 'en',
  setLang: () => {},
  t: (key) => resources.en[key] || key,
});

export const LanguageProvider = ({ children }) => {
  const [lang, setLang] = useState('en');
  const t = (key) => resources[lang][key] || key;

  return (
    <LanguageContext.Provider value={{ lang, setLang, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

