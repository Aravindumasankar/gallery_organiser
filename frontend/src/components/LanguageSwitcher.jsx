import React, { useContext } from 'react';
import { LanguageContext } from '../i18n';

const LanguageSwitcher = () => {
  const { lang, setLang, t } = useContext(LanguageContext);

  return (
    <select
      aria-label={t('switch_language')}
      value={lang}
      onChange={(e) => setLang(e.target.value)}
    >
      <option value="en">English</option>
      <option value="es">Español</option>
    </select>
  );
};

export default LanguageSwitcher;

