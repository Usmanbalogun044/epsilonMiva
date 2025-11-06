<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Routing\Controller;
use App\Models\SurveyQuestion;
use App\Models\Survey;
use Illuminate\Support\Facades\Auth;

class SurveyWebController extends Controller
{
    protected array $allowed = ['agree', 'disagree', 'neutral', 'strongly agree'];

    public function show(Request $request)
    {
        $questions = SurveyQuestion::with('options')->orderBy('order')->get();
        $user = $request->user();
        $saved = $user ? $user->survey : null;

        return view('survey', [
            'questions' => $questions,
            'saved_answers' => $saved ? [
                'q1' => $saved->q1,
                'q2' => $saved->q2,
                'q3' => $saved->q3,
                'q4' => $saved->q4,
            ] : null,
        ]);
    }

    public function submit(Request $request)
    {
        $data = $request->validate([
            'q1' => ['required'],
            'q2' => ['required'],
            'q3' => ['required'],
            'q4' => ['required'],
        ]);

        $valueMap = [
            1 => 'agree',
            2 => 'disagree',
            3 => 'neutral',
            4 => 'strongly agree',
        ];

        $normalize = function ($val) use ($valueMap) {
            if (is_numeric($val)) {
                $int = intval($val);
                return $valueMap[$int] ?? null;
            }
            $label = strtolower(trim((string) $val));
            $label = str_replace('_', ' ', $label);
            return $label;
        };

        $answers = [];
        foreach (['q1','q2','q3','q4'] as $q) {
            $answers[$q] = $normalize($data[$q]);
            if (! in_array($answers[$q], $this->allowed, true)) {
                return back()->withErrors(["{$q}" => "Invalid answer for {$q}. Allowed: " . implode(', ', $this->allowed)]);
            }
        }

        $user = $request->user();
        if (! $user) {
            return redirect()->route('login');
        }

        $survey = Survey::updateOrCreate(
            ['user_id' => $user->id],
            array_merge(['user_id' => $user->id], $answers)
        );

        $counts = [
            'agree' => 0,
            'strongly agree' => 0,
            'disagree' => 0,
            'neutral' => 0,
        ];
        foreach ($answers as $a) {
            if (isset($counts[$a])) {
                $counts[$a]++;
            }
        }

        $agreeTotal = $counts['agree'] + $counts['strongly agree'];

        if ($agreeTotal >= 3) {
            $message = 'You learn best when lessons are calm, clear, and balanced.';
        } elseif ($counts['disagree'] >= 3) {
            $message = 'You prefer hands-on, active or social learning — try workshops, labs, or group activities.';
        } elseif ($counts['neutral'] >= 3) {
            $message = 'You are flexible in your learning — a balanced mix of formats works well for you.';
        } else {
            $max = max($counts);
            $tops = array_keys($counts, $max, true);
            if (in_array('agree', $tops, true) || in_array('strongly agree', $tops, true)) {
                $message = 'You learn best when lessons are calm, clear, and balanced.';
            } elseif (in_array('disagree', $tops, true)) {
                $message = 'You prefer hands-on, active or social learning — try workshops, labs, or group activities.';
            } else {
                $message = 'You are flexible in your learning — a balanced mix of formats works well for you.';
            }
        }

        return redirect()->route('survey.show')->with(['result_message' => $message, 'counts' => $counts]);
    }
}
