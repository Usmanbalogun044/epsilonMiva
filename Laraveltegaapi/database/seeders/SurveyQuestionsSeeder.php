<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use Carbon\Carbon;

class SurveyQuestionsSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $now = Carbon::now();

        $questions = [
            ['text' => 'I find it easier to learn with pictures and videos', 'order' => 1],
            ['text' => 'Short practice sessions work better for me than long ones', 'order' => 2],
            ['text' => 'I like step-by-step guidance when learning something new', 'order' => 3],
            ['text' => 'I prefer learning at my own pace with personalized tips', 'order' => 4],
        ];

        // Insert questions and capture their IDs
        foreach ($questions as $q) {
            $questionId = DB::table('survey_questions')->insertGetId([
                'text' => $q['text'],
                'order' => $q['order'],
                'created_at' => $now,
                'updated_at' => $now,
            ]);

            // Insert options for each question using the user's specified mapping:
            // 1 => agree, 2 => disagree, 3 => neutral, 4 => strongly agree
            $options = [
                ['label' => 'Agree', 'value' => 1],
                ['label' => 'Disagree', 'value' => 2],
                ['label' => 'Neutral', 'value' => 3],
                ['label' => 'Strongly agree', 'value' => 4],
            ];

            foreach ($options as $opt) {
                DB::table('survey_options')->insert([
                    'survey_question_id' => $questionId,
                    'label' => $opt['label'],
                    'value' => $opt['value'],
                    'created_at' => $now,
                    'updated_at' => $now,
                ]);
            }
        }
    }
}
