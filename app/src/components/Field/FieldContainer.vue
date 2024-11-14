<template>
    <div>
        <!-- @slot Komponen field untuk ditampilkan -->
        <slot v-if="label === undefined" />
        <v-row v-else>
            <v-col md="3">
                <!-- @slot Label field -->
                <slot name="label" v-bind="{ label }" />
            </v-col>
            <v-col :md="md">
                <!-- @slot Komponen field untuk ditampilkan -->
                <slot />
            </v-col>
            <slot name="append-after" />
        </v-row>
    </div>
</template>

<script src="./js/FieldContainer.js"></script>

<style scoped>

</style>
