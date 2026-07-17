class WordManager {
    constructor() {
        this.wordbooks = {};
        this.customWordbooks = [];
        this.staticIndex = null;
        this.staticLoaded = false;
        this.basePath = '../words/static/';
    }

    loadJSONSync(url) {
        try {
            const xhr = new XMLHttpRequest();
            xhr.open('GET', url, false);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(null);
            if (xhr.status === 200 || (xhr.status === 0 && xhr.responseText)) {
                return JSON.parse(xhr.responseText);
            }
        } catch (e) {
            console.warn('同步加载失败:', url, e);
        }
        return null;
    }

    async loadJSONAsync(url) {
        try {
            const response = await fetch(url);
            if (response.ok) {
                return await response.json();
            }
        } catch (e) {
            console.warn('异步加载失败:', url, e);
        }
        return null;
    }

    loadStaticIndex() {
        const url = `${this.basePath}index.json`;
        
        let data = this.loadJSONSync(url);
        if (data) {
            this.staticIndex = data;
            this.staticLoaded = true;
            return data;
        }
        
        return null;
    }

    loadWordbookFromStatic(name) {
        if (!this.staticLoaded) {
            this.loadStaticIndex();
        }
        
        if (!this.staticIndex) return null;
        
        const book = this.staticIndex.wordbooks.find(b => b.name === name);
        if (!book) return null;
        
        const url = `${this.basePath}${book.file}`;
        const words = this.loadJSONSync(url);
        
        if (words) {
            this.wordbooks[name] = words;
            return words;
        }
        
        return null;
    }

    loadAllStaticWordbooks() {
        if (!this.staticLoaded) {
            this.loadStaticIndex();
        }
        
        if (!this.staticIndex) return;
        
        for (const book of this.staticIndex.wordbooks) {
            if (!this.wordbooks[book.name]) {
                this.loadWordbookFromStatic(book.name);
            }
        }
    }

    loadDefaultWordbooks() {
        this.loadAllStaticWordbooks();
        return this.wordbooks;
    }

    loadWordbook(name, path) {
        return this.loadWordbookFromStatic(name);
    }

    loadCustomWordbooks(customList) {
        this.customWordbooks = [];
        
        for (const book of customList) {
            this.customWordbooks.push({
                name: book.name,
                id: `custom_${book.name.toLowerCase().replace(/\s+/g, '_')}`,
                words: book.words,
                isCustom: true
            });
        }
        
        return this.customWordbooks;
    }

    getAllWordbooks() {
        const result = [];
        
        if (this.staticIndex) {
            for (const book of this.staticIndex.wordbooks) {
                if (this.wordbooks[book.name]) {
                    result.push({
                        name: book.name,
                        label: book.label || book.name,
                        words: this.wordbooks[book.name],
                        isCustom: false,
                        isDefault: book.isDefault || false
                    });
                }
            }
        }
        
        result.push(...this.customWordbooks);
        return result;
    }

    getWordbook(name) {
        return this.wordbooks[name] || 
               this.customWordbooks.find(b => b.id === name || b.name === name)?.words ||
               null;
    }

    getWordbookInfo(name) {
        if (this.staticIndex) {
            const book = this.staticIndex.wordbooks.find(b => b.name === name);
            if (book && this.wordbooks[name]) {
                return {
                    name: name,
                    label: book.label || name,
                    wordCount: this.wordbooks[name].length,
                    isCustom: false,
                    isDefault: book.isDefault || false
                };
            }
        }
        
        const custom = this.customWordbooks.find(b => b.id === name || b.name === name);
        if (custom) {
            return {
                name: custom.id,
                label: custom.name,
                wordCount: custom.words.length,
                isCustom: true
            };
        }
        
        return null;
    }

    addCustomWordbook(name, words) {
        const id = `custom_${name.toLowerCase().replace(/\s+/g, '_')}`;
        
        this.customWordbooks.push({
            name: name,
            id: id,
            words: words,
            isCustom: true
        });
        
        return id;
    }

    removeCustomWordbook(id) {
        const index = this.customWordbooks.findIndex(b => b.id === id);
        if (index !== -1) {
            this.customWordbooks.splice(index, 1);
            return true;
        }
        return false;
    }

    validateWord(wordData) {
        return wordData && 
               typeof wordData.word === 'string' && 
               wordData.word.trim() !== '' &&
               typeof wordData.chinese === 'string' &&
               wordData.chinese.trim() !== '';
    }

    parseCustomWords(text) {
        const words = [];
        const lines = text.split('\n');
        
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i].trim();
            if (!line) continue;
            
            const parts = line.split(/[\t,，|]/);
            if (parts.length >= 2) {
                const word = parts[0].trim();
                const chinese = parts[1].trim();
                const emoji = parts[2] ? parts[2].trim() : '📖';
                
                if (word && chinese) {
                    words.push({ word, chinese, emoji });
                }
            }
        }
        
        return words;
    }
}