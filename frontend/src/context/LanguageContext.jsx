import { useCallback, useEffect, useState } from 'react'
import { translations } from '../i18n/translations'
import { LanguageContext } from './language-context'

function initialLanguage() {
  const saved = localStorage.getItem('portfolio-language')
  if (saved === 'en' || saved === 'es') return saved
  return navigator.language.toLowerCase().startsWith('es') ? 'es' : 'en'
}

export function LanguageProvider({ children }) {
  const [language, setLanguage] = useState(initialLanguage)

  useEffect(() => {
    localStorage.setItem('portfolio-language', language)
    document.documentElement.lang = language
  }, [language])

  const t = useCallback((key) => translations[language][key] ?? translations.en[key] ?? key, [language])
  return <LanguageContext.Provider value={{ language, setLanguage, t }}>{children}</LanguageContext.Provider>
}
