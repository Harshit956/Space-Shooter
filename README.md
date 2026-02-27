# 🚀 Space Shooter (Arcade 3.3.3)

A 2D top-down space shooter built using **Python** and **Arcade 3.3.3**.

The player can move, rotate toward the mouse, shoot bullets, and survive waves of enemies (normal + shooter types).  
The core gameplay works — but the project is **not optimized** and currently has structural issues.

---

## ⚠️ Current State

- The project **needs optimization**
- Asset loading is not handled efficiently
- Sprite handling needs restructuring
- Some parts were accidentally broken during refactoring
- I honestly don’t know how to fix everything cleanly right now

So yes — this project needs help.

Any contribution is welcome.

---

## 🛠 What Needs Work

- Proper SpriteList architecture (Arcade 3.x standard)
- Asset preloading & memory cleanup
- Collision optimization
- Code restructuring (remove redundant manual loops)
- Performance tuning
- Boss logic improvements (future feature)
- Cleaner file structure

---

## 📦 Requirements

Install dependencies using:
`pip install -r requirements.txt`

### Versions Used

arcade==3.3.3  
attrs==25.4.0  
cffi==2.0.0  
pillow==11.3.0  
pycparser==3.0  
pyglet==2.1.13  
pymunk==6.9.0  
pytiled_parser==2.2.9  
typing_extensions==4.15.0  

---

## ▶️ How to Run

python "Space Shooter.py"

Make sure:
- Python 3.10+ is installed  
- Assets folder exists  
- Required textures are available  

---

## 🤝 Contributions

If you:
- Know Arcade 3.x properly  
- Can optimize Sprite handling  
- Can improve structure  
- Or just want to clean up messy code  

You’re welcome.

Open a PR. Fix what I broke. Improve what I missed.

---

## 📌 Notes

This project is still experimental and under development.  
Expect rough edges.
