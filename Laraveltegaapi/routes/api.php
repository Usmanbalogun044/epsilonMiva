<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\AuthController;
Route::post('register', [AuthController::class, 'register']);
Route::post('login', [AuthController::class, 'login']);

use App\Http\Controllers\Api\SurveyController;

Route::middleware('auth:api')->group(function () {
    Route::post('/logout', [AuthController::class, 'logout']);
    Route::get('/user', [AuthController::class, 'me']);

    // Survey endpoints
    Route::get('/survey', [SurveyController::class, 'show']);
    Route::post('/survey', [SurveyController::class, 'store']);
});
