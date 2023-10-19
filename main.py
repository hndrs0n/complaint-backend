from infrastructure.web import app

def main():
    return app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
