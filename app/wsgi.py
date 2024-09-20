from app import create_app

g_app = create_app()
if __name__ == '__main__':
    
    g_app.run()