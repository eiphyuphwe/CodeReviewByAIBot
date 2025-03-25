package com.example.codereviewbyaibot.dummy

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Surface

import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color

class SampleActivity : ComponentActivity() {
    private val viewModel = MainViewModel()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Passing Activity into ViewModel, breaking more rules
        viewModel.prepareText(this)
        setContent {
            // Ideally, it should be collectAsStateWithLifecycle
            // MaterialTheme is not used here, neither in MainScreen
            Surface(
                modifier = Modifier.fillMaxSize(),
                // Color could be part of resources / theme
                color = Color(0xFFFFFFFF)
            ) {
                MainScreen(viewModel::loadState)
            }
        }
    }
}
