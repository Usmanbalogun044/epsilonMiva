<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\SurveyWebController;

Route::get('/', function () {
    return view('welcome');
});

// Web authentication routes (session-based)
use App\Http\Controllers\AuthWebController;

Route::middleware('guest')->group(function () {
    Route::get('/login', [AuthWebController::class, 'showLogin'])->name('login');
    Route::post('/login', [AuthWebController::class, 'doLogin'])->name('login.attempt');
    Route::get('/register', [AuthWebController::class, 'showRegister'])->name('register');
    Route::post('/register', [AuthWebController::class, 'doRegister'])->name('register.attempt');
});

Route::post('/logout', [AuthWebController::class, 'logout'])->name('logout')->middleware('auth:web');

// Survey web routes (require authentication using web guard because surveys are tied to users)
Route::middleware('auth:web')->group(function () {
    Route::get('/survey', [SurveyWebController::class, 'show'])->name('survey.show');
    Route::post('/survey', [SurveyWebController::class, 'submit'])->name('survey.submit');
});
