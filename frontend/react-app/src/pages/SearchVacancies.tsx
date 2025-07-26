import React, { useState } from 'react';
import './SearchVacancies.css';

const SEARCH_MODES = [
  'Простой поиск',
  'Расширенный поиск',
  'Поиск по фильтрам',
];

function SearchVacancies() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [searchMode, setSearchMode] = useState(SEARCH_MODES[0]);
  const [showParams, setShowParams] = useState(false);
  const [query, setQuery] = useState('');

  return (
    <div className="search-vacancies-root">
      {/* Меню-гормошка */}
      <div className={`side-menu${menuOpen ? ' open' : ''}`}>
        <button className="menu-toggle" onClick={() => setMenuOpen(!menuOpen)}>
          ☰
        </button>
        <nav className="menu-content">
          <button>Профиль</button>
          <button>МДМ</button>
        </nav>
      </div>

      {/* Центральная часть */}
      <div className="search-center">
        <div className="search-bar-block">
          <div className="search-bar-buttons">
            <button className="search-mode-btn" onClick={() => {
              const idx = (SEARCH_MODES.indexOf(searchMode) + 1) % SEARCH_MODES.length;
              setSearchMode(SEARCH_MODES[idx]);
            }}>{searchMode}</button>
            <button className="params-btn" onClick={() => setShowParams(true)}>Параметры</button>
            <button className="search-btn">🔍</button>
          </div>
          <input
            className="search-input"
            type="text"
            placeholder="Введите запрос..."
            value={query}
            onChange={e => setQuery(e.target.value)}
          />
        </div>
      </div>

      {/* Модальное окно параметров */}
      {showParams && (
        <div className="modal-backdrop" onClick={() => setShowParams(false)}>
          <div className="modal-window" onClick={e => e.stopPropagation()}>
            <h2>Параметры поиска</h2>
            {/* Здесь будет форма параметров */}
            <div style={{margin: '24px 0', color: '#888'}}>Параметры появятся позже</div>
            <button className="confirm-btn" onClick={() => setShowParams(false)}>Подтвердить</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default SearchVacancies; 