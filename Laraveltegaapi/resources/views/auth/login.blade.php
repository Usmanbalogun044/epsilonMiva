<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Sign in — Tega</title>

        {{-- Link to your compiled CSS (public/css/app.css) --}}
        <link rel="stylesheet" href="{{ asset('index.css') }}" />
    </head>
    <body class="theme-peach">
        <main id="app">
            <section id="screen-login" class="screen active" aria-labelledby="login-title">
                <div class="container narrow">
                    <div class="auth-card" role="form" aria-labelledby="login-title">
                        <div class="logo-badge" aria-hidden="true">
                            <img src="{{ asset('assets/icons/Logo.svg') }}" alt="Tega logo">
                        </div>

                        <h1 id="login-title" class="headline">Welcome back</h1>
                        <p class="subhead">Sign in to continue to Tega</p>

                        {{-- Show status or validation errors --}}
                        @if (session('status'))
                            <div class="status">{{ session('status') }}</div>
                        @endif

                        @if ($errors->any())
                            <div class="errors">
                                <ul>
                                    @foreach ($errors->all() as $error)
                                        <li>{{ $error }}</li>
                                    @endforeach
                                </ul>
                            </div>
                        @endif

                        <form id="login-form" method="POST" action="{{ route('login') }}" novalidate>
                            @csrf

                            <div class="field">
                                <label class="label" for="email">Email</label>
                                <input
                                    type="email"
                                    id="email"
                                    name="email"
                                    placeholder="you@example.com"
                                    required
                                    value="{{ old('email') }}"
                                />
                                @error('email')
                                    <p class="field-error">{{ $message }}</p>
                                @enderror
                            </div>

                            <div class="field">
                                <label class="label" for="password">Password</label>
                                <input
                                    type="password"
                                    id="password"
                                    name="password"
                                    placeholder="Enter your password"
                                    required
                                />
                                @error('password')
                                    <p class="field-error">{{ $message }}</p>
                                @enderror
                            </div>

                            <div class="remember-row">
                                <label class="remember">
                                    <input
                                        type="checkbox"
                                        id="remember"
                                        name="remember"
                                        {{ old('remember') ? 'checked' : '' }}
                                    />
                                    Remember me
                                </label>

                                {{-- <a class="forgot-link" href="{{ route('password.request') }}">Forgot?</a> --}}
                            </div>

                            <button type="submit" class="btn btn-primary btn-lg">Sign in</button>

                            <div class="auth-alt" style="margin-top:18px">
                                <span>Don't have an account?</span>
                                <a href="{{ route('register') }}">Create an account</a>
                            </div>
                        </form>
                    </div>
                </div>
            </section>
        </main>

        {{-- Link to your compiled JS (public/js/app.js) --}}
        <script src="{{ asset('js/app.js') }}" defer></script>
    </body>
</html>
