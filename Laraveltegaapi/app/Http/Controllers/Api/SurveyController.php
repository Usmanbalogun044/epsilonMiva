<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use App\Models\Survey;

class SurveyController extends Controller
{
    protected array $allowed = ['agree', 'disagree', 'neutral', 'strongly agree'];

    /**
     * Return the authenticated user's survey answers.
     */
    public function show(Request $request)
    {
        $user = $request->user();

        return response()->json(['survey' => $user->survey ?? null]);
    }

    /**
     * Store or update the authenticated user's survey answers.
     */
    public function store(Request $request)
    {
        $data = $request->validate([
            'q1' => ['required', 'string'],
            'q2' => ['required', 'string'],
            'q3' => ['required', 'string'],
            'q4' => ['required', 'string'],
        ]);

        $normalize = function ($val) {
            return strtolower(trim($val));
        };

        $answers = [
            'q1' => $normalize($data['q1']),
            'q2' => $normalize($data['q2']),
            'q3' => $normalize($data['q3']),
            'q4' => $normalize($data['q4']),
        ];

        // validate values
        foreach ($answers as $k => $v) {
            if (! in_array($v, $this->allowed, true)) {
                return response()->json([
                    'message' => "Invalid answer for {$k}. Allowed: " . implode(', ', $this->allowed),
                ], Response::HTTP_UNPROCESSABLE_ENTITY);
            }
        }

        $user = $request->user();

        // create or update the user's survey row
        $survey = Survey::updateOrCreate(
            ['user_id' => $user->id],
            array_merge(['user_id' => $user->id], $answers)
        );

        return response()->json(['survey' => [
            'q1' => $survey->q1,
            'q2' => $survey->q2,
            'q3' => $survey->q3,
            'q4' => $survey->q4,
        ]]);
    }
}
