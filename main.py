import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Smart Contract Assistant - AI Q&A for Smart Contracts"
    )
    parser.add_argument(
        "--mode",
        choices=["ui", "api"],
        default="ui",
        help="Launch mode: 'ui' for Gradio interface, 'api' for FastAPI server (default: ui)",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind to (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=7860,
        help="Port to bind to (default: 7860)",
    )

    args = parser.parse_args()

    if args.mode == "ui":
        print("🚀 Launching Smart Contract Assistant (Gradio UI)...")
        from ui.gradio_app import create_app, APP_THEME, APP_CSS

        app = create_app()
        app.launch(
            server_name=args.host,
            server_port=args.port,
            share=False,
            theme=APP_THEME,
            css=APP_CSS,
        )

    elif args.mode == "api":
        print("🚀 Launching Smart Contract Assistant (FastAPI)...")
        import uvicorn

        uvicorn.run(
            "server.api:app",
            host=args.host,
            port=args.port,
            reload=True,
        )


if __name__ == "__main__":
    main()
