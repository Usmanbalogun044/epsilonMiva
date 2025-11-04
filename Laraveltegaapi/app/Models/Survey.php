<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Survey extends Model
{
    use HasFactory;

    protected $fillable = [
        'user_id',
        'q1',
        'q2',
        'q3',
        'q4',
    ];

    /**
     * A survey belongs to a user.
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
