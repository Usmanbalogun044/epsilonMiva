<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\Session;

class SurveyController extends Controller
{
    // Show survey page
    public function index()
    {
        return view('survey');
    }

    // Store survey answers (accepts form or JSON)
    public function store(Request $request)
    {
        $validated = $request->validate([
            'answers' => 'required|array',
            'answers.*.question' => 'required|string',
            'answers.*.answer' => 'required|string',
        ]);

        // Option A: save to DB (uncomment and adjust if you have a model)
        // \App\Models\Survey::create([
        //     'user_id' => $request->user()?->id,
        //     'payload' => json_encode($validated['answers']),
        // ]);

        // Option B: save to session if you don't have a DB model yet
        Session::put('survey.answers', $validated['answers']);

        // Return JSON for AJAX clients, or redirect for normal form post
        if ($request->wantsJson() || $request->isJson()) {
            return new JsonResponse(['success' => true, 'data' => $validated['answers']], 201);
        }

        return redirect()->route('survey.thanks')->with('status', 'Survey saved');
    }

    // Optional thank-you page
    public function thanks()
    {
        return view('survey-thanks'); // create this blade or change to desired route
    }
}
