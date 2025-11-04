<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\User;

class updateController extends Controller
{
    public function update(User $user, Request $request)
    {
        $user->survey = $request->input('survey');
        $user->save();
        return  response()->json(['message' => 'Survey updated successfully.'], 200);
    }
}
